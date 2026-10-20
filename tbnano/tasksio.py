"""Task format (spec section 5.1) — compatible in spirit with TerminalBench 1.0.

    tasks/<id>/
      task.yaml        # id, level, category, instruction (<=300 tok),
                       # answer_mode: files|answer|both, max_turns, tags, seed
      setup/           # files placed in /task before the episode starts
      setup.sh         # optional: generates data deterministically (seed)
      tests/test.py    # pytest; runs after the episode; invisible to the agent
      solution.sh      # reference solution
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Optional

import yaml

from .budgets import MAX_INSTRUCTION_TOKENS, MAX_TURNS
from .tokens import Tokenizer

VALID_ANSWER_MODES = {"files", "answer", "both"}
VALID_LEVELS = {1, 2, 3, 4}


@dataclass
class TaskSpec:
    id: str
    dir: Path
    level: int
    category: str
    instruction: str
    answer_mode: str = "files"
    max_turns: int = MAX_TURNS
    tags: list[str] = field(default_factory=list)
    seed: int = 0
    origin: Optional[str] = None          # e.g. "tb1/<task-id>" for adapted tasks
    template: str = ""                    # generator archetype; test∩train = ∅
    rel_tol: float = 1e-3
    split: str = "test"

    @property
    def setup_dir(self) -> Path:
        return self.dir / "setup"

    @property
    def setup_sh(self) -> Path:
        return self.dir / "setup.sh"

    @property
    def tests_dir(self) -> Path:
        return self.dir / "tests"

    @property
    def solution_sh(self) -> Path:
        return self.dir / "solution.sh"


def load_task(task_dir: Path, split: str = "test") -> TaskSpec:
    task_dir = Path(task_dir)
    meta = yaml.safe_load((task_dir / "task.yaml").read_text())
    return TaskSpec(
        id=meta["id"],
        dir=task_dir,
        level=int(meta.get("level", 2)),
        category=meta.get("category", "misc"),
        instruction=meta["instruction"],
        answer_mode=meta.get("answer_mode", "files"),
        max_turns=min(int(meta.get("max_turns", MAX_TURNS)), MAX_TURNS),
        tags=list(meta.get("tags", [])),
        seed=int(meta.get("seed", 0)),
        origin=meta.get("origin"),
        template=str(meta.get("template", "")),
        rel_tol=float(meta.get("rel_tol", 1e-3)),
        split=meta.get("split", split),
    )


def iter_tasks(root: Path) -> Iterator[TaskSpec]:
    root = Path(root)
    for task_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        if (task_dir / "task.yaml").exists():
            yield load_task(task_dir)


def validate_task(spec: TaskSpec, tok: Tokenizer) -> list[str]:
    """Static checks: required files and budget compliance."""
    problems: list[str] = []
    if spec.level not in VALID_LEVELS:
        problems.append(f"level {spec.level} not in {sorted(VALID_LEVELS)}")
    if spec.answer_mode not in VALID_ANSWER_MODES:
        problems.append(f"answer_mode {spec.answer_mode!r} invalid")
    n = tok.count(spec.instruction)
    if n > MAX_INSTRUCTION_TOKENS:
        problems.append(f"instruction {n} tokens > {MAX_INSTRUCTION_TOKENS}")
    if not spec.tests_dir.joinpath("test.py").exists():
        problems.append("missing tests/test.py")
    if not spec.solution_sh.exists():
        problems.append("missing solution.sh")
    if spec.level == 1 and spec.max_turns > 6:
        problems.append("level-1 task has max_turns > 6")
    if not spec.template:
        problems.append("missing template field")
    return problems


def materialize_setup(spec: TaskSpec, dest: Path) -> None:
    """Build the /task directory: copy setup/ then run setup.sh if present."""
    dest = Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    if spec.setup_dir.exists():
        shutil.copytree(spec.setup_dir, dest, dirs_exist_ok=True)
    if spec.setup_sh.exists():
        subprocess.run(
            ["bash", str(spec.setup_sh.resolve())],
            cwd=dest,
            env={"PATH": "/usr/local/bin:/usr/bin:/bin", "TBNANO_SEED": str(spec.seed)},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=60,
            check=True,
        )


def task_fingerprints(spec: TaskSpec) -> set[str]:
    """Hashes of the instruction and all setup/ files — used for the
    train/test leakage check (spec 5.4)."""
    h = hashlib.sha256()
    h.update(spec.instruction.encode())
    out = {"instr:" + h.hexdigest()}
    if spec.setup_dir.exists():
        for f in sorted(spec.setup_dir.rglob("*")):
            if f.is_file():
                out.add("file:" + hashlib.sha256(f.read_bytes()).hexdigest())
    return out


def build_setup_tempdir(spec: TaskSpec) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix=f"tbnano-setup-{spec.id}-"))
    materialize_setup(spec, tmp)
    return tmp
