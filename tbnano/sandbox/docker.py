"""Docker sandbox (default): one shared image for the whole benchmark.

Unlike TerminalBench 1.0 (one image per task), tbnano uses a single image
(`tbnano-sandbox`, built from docker/Dockerfile). Each task is a directory
bind-mounted at /task in a fresh container — reset between tasks is a new
container, which is cheap (~100 ms).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Optional

from .base import ExecResult, TestResult, parse_pytest_summary

IMAGE = "tbnano-sandbox:latest"


class DockerUnavailableError(RuntimeError):
    pass


def image_exists(image: str = IMAGE) -> bool:
    res = subprocess.run(
        ["docker", "image", "inspect", image],
        capture_output=True,
    )
    return res.returncode == 0


def build_image(dockerfile: Path, image: str = IMAGE) -> None:
    res = subprocess.run(
        ["docker", "build", "-t", image, "-f", str(dockerfile), str(dockerfile.parent)],
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        raise DockerUnavailableError(
            f"docker build failed:\n{res.stdout[-2000:]}\n{res.stderr[-2000:]}"
        )


class DockerSandbox:
    def __init__(
        self,
        image: str = IMAGE,
        dockerfile: Optional[Path] = None,
        work_root: Optional[Path] = None,
        keep: bool = False,
    ):
        self.image = image
        self._dockerfile = dockerfile
        self._keep = keep
        self._root = Path(work_root or tempfile.mkdtemp(prefix="tbnano-docker-"))
        self._root.mkdir(parents=True, exist_ok=True)
        self.task_dir = self._root / "task"
        self._tests_dir = self._root / "tests"
        self._container: Optional[str] = None
        self._ensure_image()

    def _ensure_image(self) -> None:
        if image_exists(self.image):
            return
        df = self._dockerfile
        if df is None:
            cand = Path(__file__).resolve().parents[2] / "docker" / "Dockerfile"
            df = cand if cand.exists() else None
        if df is None:
            raise DockerUnavailableError(
                f"image {self.image} not found and no Dockerfile available; "
                "run `tbnano build-image` or pass --dockerfile"
            )
        build_image(df, self.image)

    # -- lifecycle ------------------------------------------------------
    def start(self, setup_dir: Path, task_id: str) -> None:
        # Tests are NOT mounted during the episode (correct answers live in
        # test.py — an agent able to `cat /tests/test.py` would cheat).
        # run_tests() spins up a separate one-shot container that mounts
        # the final /task read-only plus /tests.
        self.close_container()
        if self.task_dir.exists():
            shutil.rmtree(self.task_dir)
        shutil.copytree(setup_dir, self.task_dir, symlinks=True)
        mounts = ["-v", f"{self.task_dir}:/task"]
        name = f"tbnano-{task_id.replace('/', '-')[:40]}-{int(time.time() * 1000) % 10**9}"
        res = subprocess.run(
            [
                "docker", "run", "-d", "--rm",
                # Run as the host user so files the agent writes into the
                # bind-mounted /task stay removable by the host process.
                "-u", f"{os.getuid()}:{os.getgid()}",
                "-e", "HOME=/tmp",
                "--network", "none",
                "--memory", "1g", "--cpus", "1",
                "--name", name,
                *mounts,
                "-w", "/task",
                self.image,
                "sleep", "infinity",
            ],
            capture_output=True,
            text=True,
        )
        if res.returncode != 0:
            raise DockerUnavailableError(f"docker run failed: {res.stderr.strip()}")
        self._container = res.stdout.strip()[:12]

    def close_container(self) -> None:
        if self._container:
            subprocess.run(
                ["docker", "rm", "-f", self._container], capture_output=True
            )
            self._container = None

    def close(self) -> None:
        self.close_container()
        if not self._keep and self._root.exists():
            shutil.rmtree(self._root, ignore_errors=True)

    # -- exec -----------------------------------------------------------
    def _exec(self, cmd: str, timeout: float) -> ExecResult:
        assert self._container, "container not started"
        t0 = time.monotonic()
        try:
            proc = subprocess.run(
                [
                    "docker", "exec", "-w", "/task",
                    self._container,
                    "bash", "-lc", cmd,
                ],
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=timeout + 5,  # grace for docker exec overhead
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

    # -- tools ----------------------------------------------------------
    def run(self, cmd: str, timeout: float) -> ExecResult:
        # `timeout(1)` kills the in-container process on timeout.
        wrapped = f"timeout --signal=KILL {int(timeout) + 1} bash -lc {_shq(cmd)}"
        res = self._exec(wrapped, timeout)
        if res.exit_code in (124, 137):
            res.timed_out = True
        return res

    def read_file(self, path: str, start: int = 1, lines: int = 60) -> dict:
        res = self._exec(
            f"python3 -c {_shq(_READ_PY)} {_shq(path)} {int(start)} {int(lines)}",
            timeout=15,
        )
        import json

        try:
            return json.loads(res.stdout.strip().splitlines()[-1])
        except Exception:
            return {"error": f"read_file failed: {res.stdout[-300:]} {res.stderr[-300:]}"}

    def write_file(self, path: str, content: str) -> dict:
        import base64
        import json

        b64 = base64.b64encode(content.encode()).decode()
        res = self._exec(
            f"python3 -c {_shq(_WRITE_PY)} {_shq(path)} {_shq(b64)}",
            timeout=15,
        )
        try:
            return json.loads(res.stdout.strip().splitlines()[-1])
        except Exception:
            return {"ok": False, "error": res.stderr[-300:] or res.stdout[-300:]}

    def write_submission(self, answer: str) -> None:
        self.write_file("/task/.submission/answer.txt", answer)

    def run_tests(self, tests_dir: Path, timeout: float) -> TestResult:
        # Fresh one-shot container: final /task mounted read-only + the
        # task's tests mounted read-only at /tests. The episode container
        # never saw the tests, and the test container cannot mutate /task.
        if self._tests_dir.exists():
            shutil.rmtree(self._tests_dir)
        shutil.copytree(tests_dir, self._tests_dir)
        t0 = time.monotonic()
        try:
            proc = subprocess.run(
                [
                    "docker", "run", "--rm",
                    "-u", f"{os.getuid()}:{os.getgid()}",
                    "-e", "HOME=/tmp",
                    "-e", f"TBNANO_TASK_DIR=/task",
                    "--network", "none",
                    "-v", f"{self.task_dir}:/task:ro",
                    "-v", f"{self._tests_dir}:/tests_src:ro",
                    "-w", "/task",
                    self.image,
                    "bash", "-lc",
                    "cp -r /tests_src /tmp/tests && cd /tmp/tests && "
                    "PYTHONDONTWRITEBYTECODE=1 python3 -m pytest /tmp/tests "
                    "-v --no-header -p no:cacheprovider "
                    "-o 'python_files=test.py test_*.py' --tb=line 2>&1 | tail -c 8000",
                ],
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=timeout + 15,
            )
            res = ExecResult(
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                elapsed=time.monotonic() - t0,
            )
        except subprocess.TimeoutExpired as e:
            res = ExecResult(
                exit_code=124,
                stdout=e.stdout or "",
                stderr=(e.stderr or "") + f"\n[tbnano: killed after {timeout}s]",
                elapsed=time.monotonic() - t0,
                timed_out=True,
            )
        out = res.stdout + res.stderr
        tr = parse_pytest_summary(out)
        if tr.total == 0 and res.exit_code != 0:
            tr.error = f"pytest exited {res.exit_code}: {out[-500:]}"
        return tr


def _shq(s: str) -> str:
    return "'" + s.replace("'", "'\"'\"'") + "'"


_READ_PY = """\
import sys, json
p, start, lines = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
try:
    text = open(p, errors='replace').read()
except OSError as e:
    print(json.dumps({'error': f'{type(e).__name__}: {e}'})); sys.exit()
ls = text.splitlines(keepends=True)
start = max(1, start)
print(json.dumps({'text': ''.join(ls[start-1:start-1+lines]), 'total_lines': len(ls)}))
"""

_WRITE_PY = """\
import sys, json, base64
p, b64 = sys.argv[1], sys.argv[2]
import os
os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
data = base64.b64decode(b64)
open(p, 'wb').write(data)
print(json.dumps({'ok': True, 'bytes': len(data)}))
"""
