"""Local sandbox (--sandbox local): tempdir + subprocess with rlimits.

Debug/development mode (the spec reserves it for quick iteration on a
laptop, not for official numbers): there is no real network isolation and
no container boundary, but command timeout, path containment under /task,
cwd=/task and empty stdin are enforced the same as in docker mode.
"""

from __future__ import annotations

import os
import resource
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

from .base import ExecResult, TestResult, finalize_test_result


def _limits() -> None:
    # Runs in the child right before exec.
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    resource.setrlimit(resource.RLIMIT_FSIZE, (256 << 20, 256 << 20))
    # NOTE: no RLIMIT_NPROC — it counts the uid's processes system-wide,
    # which would make parallel local runs fork-fail.


class LocalSandbox:
    def __init__(self, work_root: Optional[Path] = None, keep: bool = False):
        self._root = Path(work_root or tempfile.mkdtemp(prefix="tbnano-"))
        self._root.mkdir(parents=True, exist_ok=True)
        self._keep = keep
        self.task_dir: Path = self._root / "task"
        self._tests_dir: Optional[Path] = None

    # -- lifecycle ------------------------------------------------------
    def start(self, setup_dir: Path, task_id: str) -> None:
        # Tests are NOT placed in the sandbox during the episode: the agent
        # must not see them (correct answers live in test.py). They are
        # staged only inside run_tests(), after the episode ends.
        if self.task_dir.exists():
            shutil.rmtree(self.task_dir)
        shutil.copytree(setup_dir, self.task_dir, symlinks=True)

    def close(self) -> None:
        if not self._keep and self._root.exists():
            shutil.rmtree(self._root, ignore_errors=True)

    # -- containment ----------------------------------------------------
    def _resolve(self, path: str) -> Path:
        p = Path(path)
        if not p.is_absolute():
            p = self.task_dir / p
        elif str(p).startswith("/task"):
            p = self.task_dir / str(p)[len("/task"):].lstrip("/")
        resolved = p.resolve()
        if not str(resolved).startswith(str(self.task_dir.resolve())):
            raise PermissionError(f"path escapes /task: {path}")
        return resolved

    # -- tools ----------------------------------------------------------
    def run(self, cmd: str, timeout: float) -> ExecResult:
        # Keep the real HOME so user-site packages (e.g. pytest) resolve;
        # local mode is a debug sandbox, not a security boundary.
        # HOME is the task dir itself: the agent cannot read or damage the
        # real home directory. PYTHONPATH carries user-site packages
        # (pytest) that a real HOME would have resolved.
        user_site = os.path.expanduser(
            f"~/.local/lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages"
        )
        env = {
            "PATH": os.path.expanduser("~/.local/bin")
            + ":/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin",
            "HOME": str(self.task_dir),
            "PYTHONPATH": user_site,
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TERM": "dumb",
            "TBNANO_TASK_DIR": str(self.task_dir),
        }
        t0 = time.monotonic()
        try:
            proc = subprocess.run(
                ["bash", "-lc", cmd],
                cwd=self.task_dir,
                env=env,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True, errors="replace",
                timeout=timeout,
                preexec_fn=_limits,
            )
            return ExecResult(
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                elapsed=time.monotonic() - t0,
            )
        except subprocess.TimeoutExpired as e:
            return ExecResult(
                exit_code=124,
                stdout=e.stdout or "",
                stderr=(e.stderr or "") + f"\n[tbnano: killed after {timeout}s]",
                elapsed=time.monotonic() - t0,
                timed_out=True,
            )

    def read_file(self, path: str, start: int = 1, lines: int = 60) -> dict:
        try:
            p = self._resolve(path)
            text = p.read_text(errors="replace")
        except (FileNotFoundError, PermissionError, IsADirectoryError, OSError) as e:
            return {"error": f"{type(e).__name__}: {e}"}
        all_lines = text.splitlines(keepends=True)
        start = max(1, int(start))
        slice_ = all_lines[start - 1 : start - 1 + int(lines)]
        return {"text": "".join(slice_), "total_lines": len(all_lines)}

    def write_file(self, path: str, content: str) -> dict:
        try:
            p = self._resolve(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
            return {"ok": True, "bytes": len(content.encode())}
        except (PermissionError, IsADirectoryError, OSError) as e:
            return {"ok": False, "error": f"{type(e).__name__}: {e}"}

    def write_submission(self, answer: str) -> None:
        sub = self.task_dir / ".submission"
        sub.mkdir(parents=True, exist_ok=True)
        (sub / "answer.txt").write_text(answer)

    def run_tests(self, tests_dir: Path, timeout: float) -> TestResult:
        # Stage tests only now — after the episode — so they never sat in
        # the agent's filesystem while it acted.
        self._tests_dir = self._root / ".tests"
        if self._tests_dir.exists():
            shutil.rmtree(self._tests_dir)
        shutil.copytree(tests_dir, self._tests_dir)
        # Tests are harness code, not agent code: run them with the harness
        # interpreter (which has pytest), not whatever python3 the sanitized
        # agent PATH finds (macOS /usr/bin/python3 has no pytest).
        env = {**os.environ, "TBNANO_TASK_DIR": str(self.task_dir), "PYTHONDONTWRITEBYTECODE": "1"}
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", str(self._tests_dir), "-v", "--no-header",
                 "-p", "no:cacheprovider", "-o", "python_files=test.py test_*.py", "--tb=line"],
                cwd=self.task_dir, env=env, stdin=subprocess.DEVNULL,
                capture_output=True, text=True, errors="replace", timeout=timeout,
            )
            code, out = proc.returncode, (proc.stdout + proc.stderr)[-8000:]
        except subprocess.TimeoutExpired as e:
            code, out = 124, str(e.stdout or "")[-8000:] + f"\n[tbnano: tests killed after {timeout}s]"
        return finalize_test_result(out, code)
