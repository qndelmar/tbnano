"""`tbnano validate` — spec 8.1/8.2 benchmark validation.

For every task:
  1. static checks (files present, instruction <= 300 tokens, level rules)
  2. ORACLE run: solution.sh replayed line-by-line through the real
     episode loop (scripted backend + json_tags adapter) — so reference
     solutions are checked *as agent trajectories* under every budget:
     max_turns, context <= 8192, exec <= 60 s.
  3. EMPTY run: tests without any agent action — must NOT resolve.

A task is VALID iff: static ok AND oracle resolves AND empty fails.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .adapters import get_adapter
from .backends.scripted import ScriptedBackend
from .episode import run_episode
from .runner import split_script
from .sandbox import make_sandbox
from .tasksio import (
    TaskSpec,
    build_setup_tempdir,
    task_fingerprints,
    validate_task,
)
from .tokens import ApproxTokenizer, Tokenizer


@dataclass
class TaskVerdict:
    task_id: str
    ok: bool
    oracle_resolved: bool
    empty_fails: bool
    problems: list[str]
    oracle_end_reason: str = ""


def validate_one(
    spec: TaskSpec,
    sandbox_kind: str = "local",
    tok: Optional[Tokenizer] = None,
    sandbox_kwargs: Optional[dict] = None,
) -> TaskVerdict:
    tok = tok or ApproxTokenizer()
    problems = validate_task(spec, tok)
    adapter = get_adapter("json_tags")

    # --- oracle run ----------------------------------------------------
    oracle_ok, oracle_end = False, "not_run"
    setup_dir = build_setup_tempdir(spec)
    sb = make_sandbox(sandbox_kind, **(sandbox_kwargs or {}))
    try:
        sb.start(setup_dir, spec.tests_dir, spec.id)
        backend = ScriptedBackend(script="oracle")
        backend.set_oracle(split_script(spec.solution_sh.read_text()))
        ep = run_episode(spec, backend, adapter, sb, tok)
        oracle_end = ep.end_reason
        sb.write_submission(ep.answer)
        tests = sb.run_tests(timeout=60.0)
        oracle_ok = tests.resolved
        if ep.end_reason != "finish":
            problems.append(f"oracle ended as {ep.end_reason}")
        if not oracle_ok:
            problems.append(
                f"solution.sh fails tests ({tests.passed}/{tests.total} passed; "
                f"{tests.error or ''} {tests.output[-200:]})"
            )

        # --- empty run ---------------------------------------------------
        sb.start(setup_dir, spec.tests_dir, spec.id)  # fresh copy
        sb.write_submission("")
        empty_tests = sb.run_tests(timeout=60.0)
        empty_fails = not empty_tests.resolved
        if not empty_fails:
            problems.append("tests pass with EMPTY solution")
    finally:
        sb.close()

    ok = not problems
    return TaskVerdict(
        task_id=spec.id,
        ok=ok,
        oracle_resolved=oracle_ok,
        empty_fails=empty_fails,
        problems=problems,
        oracle_end_reason=oracle_end,
    )


def check_leakage(
    test_specs: list[TaskSpec],
    train_root: Path,
) -> tuple[bool, set[str]]:
    """Hash every test instruction + setup file; none may appear in train."""
    from .tasksio import iter_tasks

    test_fp: set[str] = set()
    for s in test_specs:
        test_fp |= task_fingerprints(s)
    train_fp: set[str] = set()
    for s in iter_tasks(train_root):
        train_fp |= task_fingerprints(s)
    overlap = test_fp & train_fp
    return (len(overlap) == 0, overlap)


def validate_all(
    specs: list[TaskSpec],
    sandbox_kind: str = "local",
    jobs: int = 4,
    check_leak: bool = False,
    train_root: Optional[Path] = None,
) -> dict:
    tok = ApproxTokenizer()
    verdicts: list[TaskVerdict] = []
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futs = {
            pool.submit(validate_one, s, sandbox_kind, tok): s for s in specs
        }
        for f in as_completed(futs):
            v = f.result()
            verdicts.append(v)
            if not v.ok:
                print(f"  FAIL {v.task_id}: {'; '.join(v.problems)}", flush=True)

    n = len(verdicts)
    valid = sum(1 for v in verdicts if v.ok)
    oracle_resolved = sum(1 for v in verdicts if v.oracle_resolved)
    leak_ok, overlap = (True, set())
    if check_leak and train_root:
        leak_ok, overlap = check_leakage(specs, Path(train_root))

    summary = {
        "n_tasks": n,
        "valid": valid,
        "oracle_resolved": oracle_resolved,
        "oracle_rate": oracle_resolved / n if n else 0.0,
        "leak_free": leak_ok,
        "leak_overlap_count": len(overlap),
        "bad": [
            {"id": v.task_id, "problems": v.problems} for v in verdicts if not v.ok
        ],
    }
    return summary
