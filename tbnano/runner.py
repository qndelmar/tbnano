"""Runner: episodes over the task set, parallel via --jobs N.

Per (task, sample): fresh /task from the task's setup, a fresh sandbox
container/dir, the episode loop, then pytest verification and a
runs/<model>/<task>.jsonl trajectory.
"""

from __future__ import annotations

import json
import re
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Optional

from .adapters import Adapter
from .backends.base import Backend
from .episode import EpisodeResult, run_episode
from .metrics import RunRecord, aggregate, format_table, write_report
from .sandbox import make_sandbox
from .tasksio import TaskSpec, build_setup_tempdir
from .tokens import ApproxTokenizer, Tokenizer


def split_script(script: str) -> list[str]:
    """Split a solution.sh into logical commands.

    Comments, blanks and `set ...` lines are dropped. A heredoc block or a
    command spanning multiple lines inside quotes (e.g. `python3 -c "..."`)
    stays a single command so it can go through one run() call.
    """
    commands: list[str] = []
    cur: list[str] = []
    heredoc_end: Optional[str] = None

    def quotes_open(text: str) -> bool:
        in_s = in_d = False
        esc = False
        for ch in text:
            if esc:
                esc = False
                continue
            if ch == "\\" and not in_s:
                esc = True
            elif ch == "'" and not in_d:
                in_s = not in_s
            elif ch == '"' and not in_s:
                in_d = not in_d
        return in_s or in_d

    for line in script.splitlines():
        stripped = line.strip()
        if heredoc_end is not None:
            cur.append(line)
            if stripped == heredoc_end:
                commands.append("\n".join(cur))
                cur = []
                heredoc_end = None
            continue
        if cur:  # inside an open-quoted command: keep consuming lines
            cur.append(line)
            if not quotes_open("\n".join(cur)):
                commands.append("\n".join(cur))
                cur = []
            continue
        if not stripped or stripped.startswith("#") or stripped.startswith("set "):
            continue
        cur.append(line)
        m = re.search(r"<<-?\s*['\"]?(\w+)['\"]?", line)
        if m:
            heredoc_end = m.group(1)
            continue
        if not quotes_open("\n".join(cur)):
            commands.append("\n".join(cur))
            cur = []
    if cur:
        commands.append("\n".join(cur))
    return commands


def run_one(
    spec: TaskSpec,
    backend: Backend,
    adapter: Adapter,
    sandbox_kind: str,
    tok: Tokenizer,
    temperature: float = 0.0,
    seed: Optional[int] = None,
    sandbox_kwargs: Optional[dict] = None,
) -> tuple[RunRecord, EpisodeResult, str]:
    """Run one episode + verification. Returns (record, episode, test_output)."""
    setup_dir = build_setup_tempdir(spec)
    sb = make_sandbox(sandbox_kind, **(sandbox_kwargs or {}))
    try:
        sb.start(setup_dir, spec.id)  # tests stay outside the sandbox
        ep = run_episode(
            spec, backend, adapter, sb, tok, temperature=temperature, seed=seed
        )
        sb.write_submission(ep.answer)
        tests = sb.run_tests(spec.tests_dir, timeout=60.0)
        rec = RunRecord(
            task_id=spec.id,
            resolved=tests.resolved,
            partial=tests.partial,
            end_reason=ep.end_reason,
            turns_used=ep.turns_used,
            tokens_used=ep.tokens_used,
            invalid_calls=ep.invalid_calls,
            exec_seconds=ep.exec_seconds,
            level=spec.level,
            category=spec.category,
            template=spec.template,
        )
        return rec, ep, tests.output
    finally:
        sb.close()


def run_benchmark(
    tasks: list[TaskSpec],
    backend_factory: Callable[[], Backend],
    adapter: Adapter,
    model_name: str,
    out_root: Path,
    sandbox_kind: str = "local",
    jobs: int = 4,
    samples: int = 1,
    temperature: float = 0.0,
    seed: Optional[int] = None,
    tok: Optional[Tokenizer] = None,
    sandbox_kwargs: Optional[dict] = None,
    progress: bool = True,
) -> Path:
    """Run all tasks x samples; write trajectories + report.json."""
    tok = tok or ApproxTokenizer()
    out_dir = Path(out_root) / model_name.replace("/", "_")
    out_dir.mkdir(parents=True, exist_ok=True)

    lock = threading.Lock()
    records: list[RunRecord] = []

    def worker(spec: TaskSpec, sample: int):
        # Stateful backends (scripted) get a fresh instance per task from
        # the factory; stateless ones (hf/api) return the shared object.
        backend = backend_factory()
        if hasattr(backend, "reset"):
            backend.reset()
        if spec.solution_sh.exists() and hasattr(backend, "set_oracle"):
            backend.set_oracle(split_script(spec.solution_sh.read_text()))
        rec, ep, test_out = run_one(
            spec, backend, adapter, sandbox_kind, tok,
            temperature=temperature,
            seed=None if seed is None else seed + sample,
            sandbox_kwargs=sandbox_kwargs,
        )
        rec.sample = sample
        traj_path = out_dir / f"{spec.id}{'.s' + str(sample) if sample else ''}.jsonl"
        with traj_path.open("w") as f:
            for entry in ep.trajectory:
                f.write(json.dumps(entry) + "\n")
            f.write(
                json.dumps(
                    {
                        "summary": {
                            **ep.summary_line(),
                            "resolved": rec.resolved,
                            "partial": rec.partial,
                            "sample": sample,
                        }
                    }
                )
                + "\n"
            )
        with lock:
            records.append(rec)
            if progress and len(records) % 10 == 0:
                print(f"  [{len(records)}/{len(tasks) * samples}]", flush=True)
        return rec

    work = [(t, s) for t in tasks for s in range(samples)]
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futs = [pool.submit(worker, t, s) for t, s in work]
        for f in as_completed(futs):
            f.result()  # propagate exceptions

    report_path = write_report(records, out_dir, model_name)
    rep = aggregate(records)
    print(format_table({model_name: {"overall": rep["overall"], "n_tasks": len(tasks)}}))
    return report_path
