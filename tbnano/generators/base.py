"""Shared helpers for task generators."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Optional

import yaml


def write_task(
    out_root: Path,
    task_id: str,
    level: int,
    category: str,
    instruction: str,
    answer_mode: str = "files",
    max_turns: int = 8,
    tags: Optional[list[str]] = None,
    seed: int = 0,
    split: str = "test",
    template: str = "",
    setup_files: Optional[dict[str, str]] = None,
    setup_sh: Optional[str] = None,
    test_py: str = "",
    solution_sh: str = "",
    origin: Optional[str] = None,
    rel_tol: Optional[float] = None,
) -> Path:
    d = Path(out_root) / task_id
    (d / "setup").mkdir(parents=True, exist_ok=True)
    (d / "tests").mkdir(parents=True, exist_ok=True)
    meta = {
        "id": task_id,
        "level": level,
        "category": category,
        "instruction": instruction,
        "answer_mode": answer_mode,
        "max_turns": max_turns,
        "tags": tags or [],
        "seed": seed,
        "split": split,
        "template": template or task_id.rsplit("-", 2)[0],
    }
    if origin:
        meta["origin"] = origin
    if rel_tol is not None:
        meta["rel_tol"] = rel_tol
    (d / "task.yaml").write_text(yaml.safe_dump(meta, allow_unicode=True, sort_keys=False))
    for rel, content in (setup_files or {}).items():
        p = d / "setup" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    if setup_sh:
        f = d / "setup.sh"
        f.write_text(setup_sh)
        f.chmod(0o755)
    (d / "tests" / "test.py").write_text(textwrap.dedent(test_py))
    sol = d / "solution.sh"
    sol.write_text(textwrap.dedent(solution_sh))
    sol.chmod(0o755)
    return d


ANSWER_TEST = """\
import os, math, re
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
ANSWER_FILE = BASE / ".submission" / "answer.txt"
EXPECTED = {expected!r}
REL_TOL = {rel_tol!r}

def _read_answer():
    env = os.environ.get("TBNANO_ANSWER")
    if env is not None:
        return env
    if ANSWER_FILE.exists():
        return ANSWER_FILE.read_text().strip()
    return ""

def _parse_number(s):
    m = re.findall(r"-?\\d+\\.?\\d*(?:[eE][-+]?\\d+)?", s)
    return float(m[-1]) if m else None

def test_answer_present():
    assert _read_answer() != "", "no answer submitted"

def test_answer_value():
    got = _parse_number(_read_answer())
    assert got is not None, f"could not parse a number from answer"
    exp = float(EXPECTED)
    assert math.isclose(got, exp, rel_tol=REL_TOL), f"got {{got}}, expected {{exp}}"
"""


def answer_test(expected: float, rel_tol: float = 1e-3) -> str:
    return ANSWER_TEST.format(expected=expected, rel_tol=rel_tol)


FILES_TEST = """\
import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = {expected!r}
OUT = {out!r}

def test_file_present():
    assert (BASE / OUT).exists(), f"{{OUT}} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
"""


def files_test(out: str, expected: str) -> str:
    """pytest body: file `out` exists and equals `expected` exactly.
    The _present check is zero-weight in `partial` (presence convention)."""
    return FILES_TEST.format(expected=expected, out=out)


def kv_test(out: str, expected: dict, rel_tol: float = 1e-6) -> str:
    return f'''\
import math, os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = {expected!r}

def test_file_present():
    assert (BASE / {out!r}).exists(), "{out} missing"

def test_kv():
    kv = {{}}
    for line in (BASE / {out!r}).read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            kv[k.strip()] = float(v)
    for k, v in EXPECTED.items():
        assert k in kv, f"{{k}} missing"
        assert math.isclose(kv[k], v, rel_tol={rel_tol!r}), f"{{k}}: {{kv[k]}} != {{v}}"
'''


def json_dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)


def pick(rng, test_pool, train_pool, split):
    """Choose from a split-disjoint name pool so test artifacts and
    instructions can never collide with train ones (spec 5.4 leak check)."""
    return rng.choice(train_pool if split == "train" else test_pool)


def with_id(content: str, task_id: str, comment: str = "#") -> str:
    """Embed a task-id comment into a script file so scaffold files are
    unique per task and per split (leak-check hygiene, spec 5.4)."""
    return f"{comment} task:{task_id}\n" + content
