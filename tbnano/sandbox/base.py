"""Sandbox interface.

Lifecycle per task:
    sb.start(setup_dir, tests_dir, task_id)  # fresh /task from the task's setup
    sb.run(cmd, timeout)                     # bash -lc in /task
    sb.read_file(path, start, lines)
    sb.write_file(path, content)
    sb.write_submission(answer)              # -> /task/.submission/answer.txt
    sb.run_tests(timeout)                    # pytest on the injected tests
    sb.close()                               # destroy the environment
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

    @property
    def resolved(self) -> bool:
        return self.error is None and self.total > 0 and self.passed == self.total

    @property
    def partial(self) -> float:
        return self.passed / self.total if self.total else 0.0


_SUMMARY_RE = re.compile(r"(\d+)\s+(passed|failed|error|skipped|xfailed|xpassed)")


def parse_pytest_summary(output: str) -> TestResult:
    counts: dict[str, int] = {}
    for n, word in _SUMMARY_RE.findall(output):
        counts[word] = counts.get(word, 0) + int(n)
    passed = counts.get("passed", 0) + counts.get("xpassed", 0)
    failed = counts.get("failed", 0) + counts.get("error", 0) + counts.get("xfailed", 0)
    total = passed + failed + counts.get("skipped", 0)
    return TestResult(passed=passed, total=total, output=output)


class Sandbox(Protocol):
    def start(self, setup_dir: Path, tests_dir: Optional[Path], task_id: str) -> None: ...
    def run(self, cmd: str, timeout: float) -> ExecResult: ...
    def read_file(self, path: str, start: int = 1, lines: int = 60) -> dict: ...
    def write_file(self, path: str, content: str) -> dict: ...
    def write_submission(self, answer: str) -> None: ...
    def run_tests(self, timeout: float) -> TestResult: ...
    def close(self) -> None: ...
