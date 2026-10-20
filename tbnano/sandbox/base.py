"""Sandbox interface.

Lifecycle per task:
    sb.start(setup_dir, task_id)  # fresh /task; tests are NOT in the sandbox
    sb.run(cmd, timeout)          # bash -lc in /task
    sb.read_file(path, start, lines)
    sb.write_file(path, content)
    sb.write_submission(answer)   # -> /task/.submission/answer.txt
    sb.run_tests(tests_dir, timeout)  # pytest, staged only after the episode
    sb.close()                    # destroy the environment
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Protocol


@dataclass
class ExecResult:
    exit_code: int
    stdout: str
    stderr: str
    elapsed: float = 0.0
    timed_out: bool = False

    def to_tool_json(self) -> str:
        import json

        out = {"exit_code": self.exit_code, "stdout": self.stdout, "stderr": self.stderr}
        if self.timed_out:
            out["timed_out"] = True
        return json.dumps(out)


@dataclass
class TestResult:
    passed: int = 0
    total: int = 0
    output: str = ""
    error: Optional[str] = None
    # Zero-weight ("presence") tests exist so `resolved` still requires a
    # submitted answer / produced file, but they must not inflate the
    # `partial` metric (a junk answer would otherwise score 50%).
    presence_passed: int = 0
    presence_total: int = 0

    @property
    def resolved(self) -> bool:
        return self.error is None and self.total > 0 and self.passed == self.total

    @property
    def partial(self) -> float:
        scored = self.total - self.presence_total
        if scored <= 0:
            return 0.0
        return (self.passed - self.presence_passed) / scored


_SUMMARY_RE = re.compile(r"(\d+)\s+(passed|failed|error|skipped|xfailed|xpassed)")
_LINE_RE = re.compile(
    r"\b([\w./-]*test[\w.-]*)::(test_\w+)\s+(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\b"
)


def is_presence_test(name: str) -> bool:
    """Convention: `test_*_present*` / `test_presence_*` checks only assert
    an artifact exists; they carry zero weight in `partial`."""
    return name.startswith("test_presence") or "_present" in name


def parse_pytest_summary(output: str) -> TestResult:
    counts: dict[str, int] = {}
    for n, word in _SUMMARY_RE.findall(output):
        counts[word] = counts.get(word, 0) + int(n)
    passed = counts.get("passed", 0) + counts.get("xpassed", 0)
    failed = counts.get("failed", 0) + counts.get("error", 0) + counts.get("xfailed", 0)
    total = passed + failed + counts.get("skipped", 0)
    tr = TestResult(passed=passed, total=total, output=output)
    # Prefer per-test lines (pytest -v): they let us weigh presence tests
    # at zero. If they are absent the summary counts stand.
    per_test = _LINE_RE.findall(output)
    if per_test:
        tr.presence_total = sum(1 for _, name, _ in per_test if is_presence_test(name))
        tr.presence_passed = sum(
            1
            for _, name, st in per_test
            if is_presence_test(name) and st in ("PASSED", "XPASS")
        )
    return tr


def finalize_test_result(output: str, exit_code: int) -> TestResult:
    """Parse pytest output; zero collected tests is always a harness error (a task with
    no runnable tests must never count as a silent 0/0)."""
    tr = parse_pytest_summary(output)
    if tr.total == 0:
        tr.error = f"no tests ran (pytest exit {exit_code}): {output[-500:]}"
    return tr


class Sandbox(Protocol):
    def start(self, setup_dir: Path, task_id: str) -> None: ...
    def run(self, cmd: str, timeout: float) -> ExecResult: ...
    def read_file(self, path: str, start: int = 1, lines: int = 60) -> dict: ...
    def write_file(self, path: str, content: str) -> dict: ...
    def write_submission(self, answer: str) -> None: ...
    def run_tests(self, tests_dir: Path, timeout: float) -> TestResult: ...
    def close(self) -> None: ...
