"""Code family (spec 5.3, ~20%): small bugs in Python/bash with tests."""

from __future__ import annotations

import random
from pathlib import Path

from .base import pick, with_id, write_task

# --- fix_python: (name, buggy_src, fixed_src, visible_cases, hidden_cases)
# A case is (args_tuple, expected).
PY_BUGS = [
    (
        "area_circle",
        "def area_circle(r):\n    return 3.14159 * r * 2\n",
        "def area_circle(r):\n    return 3.14159 * r ** 2\n",
        [((2,), 12.56636), ((5,), 78.53975)],
        [((1,), 3.14159), ((3.5,), 38.484477)],
    ),
    (
        "moving_average",
        (
            "def moving_average(xs, k):\n"
            "    return [sum(xs[i:i+k]) / k for i in range(len(xs) - k)]\n"
        ),
        (
            "def moving_average(xs, k):\n"
            "    return [sum(xs[i:i+k]) / k for i in range(len(xs) - k + 1)]\n"
        ),
        [(((1, 2, 3, 4), 2), [1.5, 2.5, 3.5])],
        [(((1, 2, 3, 4, 5), 3), [2.0, 3.0, 4.0])],
    ),
    (
        "km_to_miles",
        "def km_to_miles(km):\n    return km * 1.60934\n",
        "def km_to_miles(km):\n    return km * 0.621371\n",
        [((10,), 6.21371), ((100,), 62.1371)],
        [((42,), 26.097582)],
    ),
    (
        "sum_evens",
        (
            "def sum_evens(xs):\n"
            "    return sum(x for x in xs if x % 2 == 1)\n"
        ),
        (
            "def sum_evens(xs):\n"
            "    return sum(x for x in xs if x % 2 == 0)\n"
        ),
        [(((1, 2, 3, 4, 5, 6),), 12)],
        [(((2, 4, 7, 9, 10),), 16)],
    ),
    (
        "clamp",
        (
            "def clamp(x, lo, hi):\n"
            "    if x < lo:\n        return lo\n"
            "    if x < hi:\n        return hi\n"
            "    return x\n"
        ),
        (
            "def clamp(x, lo, hi):\n"
            "    if x < lo:\n        return lo\n"
            "    if x > hi:\n        return hi\n"
            "    return x\n"
        ),
        [((5, 0, 10), 5), ((15, 0, 10), 10)],
        [((-3, 0, 10), 0), ((11, 0, 10), 10), ((7, 2, 8), 7)],
    ),
]


def gen_fix_python(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    # Adapted from TerminalBench 1.0 "broken-python" (a single small bug,
    # error visible from the shipped checker).
    name, buggy, fixed, vis, hid = rng.choice(PY_BUGS)
    fname = pick(rng, ["calc.py", "utils.py", "ops.py"],
                 ["helpers.py", "mathx.py", "compute.py"], split)
    visible_calls = "\n".join(
        f"    print({name}({', '.join(map(repr, a[0]))}), 'expect', {a[1]!r})"
        for a in vis
    )
    check = f'''\
import sys
sys.path.insert(0, '.')
from {fname[:-3]} import {name}

def main():
{visible_calls}

if __name__ == '__main__':
    main()
'''
    asserts = []
    for a in vis + hid:
        args, exp = ", ".join(map(repr, a[0])), a[1]
        if isinstance(exp, list):
            asserts.append(
                f"    assert {name}({args}) == {exp!r}, f'{{ {name}({args}) }} != {exp!r}'"
            )
        else:
            asserts.append(
                f"    assert abs({name}({args}) - {exp!r}) < 1e-4, f'{{ {name}({args}) }} != {exp!r}'"
            )
    tid = f"fixpy-{split}-{idx:03d}"
    test = f'''\
import os, sys
sys.path.insert(0, os.environ.get('TBNANO_TASK_DIR', '/task'))
from {fname[:-3]} import {name}

def test_{name}():
{chr(10).join(asserts)}
'''
    return write_task(
        out_root, tid, level=3, category="code",
        instruction=(
            f"`python3 check.py` prints wrong results — {name}() in "
            f"{fname} is buggy. Fix {fname} so the outputs match the "
            f"'expect' values."
        ),
        answer_mode="files", max_turns=8,
        tags=["python", "bugfix"], seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: with_id(buggy, tid), "check.py": with_id(check, tid)},
        test_py=test,
        solution_sh=f"cat > {fname} <<'EOF'\n{fixed}EOF\npython3 check.py\n",
        origin="tb1/broken-python",
    )


BASH_BUGS = [
    # (buggy_cmd, fixed_cmd)
    ("grep ERR {log} > {out}\n", "grep ERROR {log} > {out}\n"),
    ("grep ERROR {log} > {out}x\n", "grep ERROR {log} > {out}\n"),
    ("grep error {log} > {out}\n", "grep ERROR {log} > {out}\n"),
    ("sort {log} | grep ERROR > {out}\n", "grep ERROR {log} > {out}\n"),
]


def gen_fix_bash(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    buggy_tpl, fixed_tpl = rng.choice(BASH_BUGS)
    logf = pick(rng, ["app.log", "sys.log"], ["jobs.log", "nodes.log"], split)
    outf = pick(rng, ["errors.txt", "errs.txt"], ["found.txt", "hits.txt"], split)
    scriptf = pick(rng, ["report.sh", "extract.sh"], ["scan.sh", "filter.sh"], split)
    buggy = buggy_tpl.format(log=logf, out=outf)
    fixed = fixed_tpl.format(log=logf, out=outf)
    target = "ERROR"
    n_lines = rng.randint(40, 120)
    k = rng.randint(3, 30)
    positions = set(rng.sample(range(n_lines), k))
    lines = []
    for i in range(n_lines):
        lvl = target if i in positions else rng.choice(["INFO", "WARN", "DEBUG"])
        lines.append(f"[{lvl}] event {i} payload")
    log = "\n".join(lines) + "\n"
    expected = "".join(l + "\n" for l in lines if l.startswith(f"[{target}]"))
    script = f"#!/bin/bash\n# produce {outf}: the ERROR lines of {logf}\n" + buggy
    tid = f"fixbash-{split}-{idx:03d}"
    return write_task(
        out_root, tid, level=3, category="code",
        instruction=(
            f"{scriptf} should write every ERROR line of {logf} into "
            f"{outf}, but running it produces the wrong result. "
            f"Fix {scriptf} and run it so {outf} is correct."
        ),
        answer_mode="files", max_turns=8,
        tags=["bash", "bugfix"], seed=rng.randint(0, 10**6), split=split,
        setup_files={logf: log, scriptf: with_id(script, tid)},
        test_py=f'''\
import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = {expected!r}

def test_errors_file():
    p = BASE / "{outf}"
    assert p.exists(), "{outf} missing — did you run {scriptf}?"
    assert p.read_text() == EXPECTED
''',
        solution_sh=f"cat > {scriptf} <<'EOF'\n#!/bin/bash\n{fixed}EOF\nbash {scriptf}\n",
    )


def gen_write_script(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    nfiles = rng.randint(3, 5)
    fname = pick(rng, ["convert.sh", "merge.sh"], ["bundle.sh", "join.sh"], split)
    header = rng.choice(["t,alt,v", "id,x,y", "ts,a,b"])
    ncols = len(header.split(","))
    files = {}
    all_rows = []
    for i in range(nfiles):
        rows = [
            [str(rng.randint(0, 999)) for _ in range(ncols)]
            for _ in range(rng.randint(5, 20))
        ]
        all_rows += rows
        files[f"data/part{i}.csv"] = header + "\n" + "\n".join(",".join(r) for r in rows) + "\n"
    all_rows.sort(key=lambda r: int(r[0]))
    expected = header + "\n" + "\n".join(",".join(r) for r in all_rows) + "\n"
    tid = f"writesh-{split}-{idx:03d}"
    return write_task(
        out_root, tid, level=4, category="code",
        instruction=(
            f"Write a script {fname} that merges all CSV files in data/ "
            f"into merged.csv: keep the shared header once, then all data "
            f"rows sorted numerically by the first column. Run it so "
            f"merged.csv exists."
        ),
        answer_mode="files", max_turns=10,
        tags=["bash", "script", "csv"], seed=rng.randint(0, 10**6), split=split,
        setup_files=files,
        test_py=f'''\
import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = {expected!r}

def test_merged():
    p = BASE / "merged.csv"
    assert p.exists(), "merged.csv missing"
    assert p.read_text() == EXPECTED
''',
        solution_sh=(
            f"cat > {fname} <<'EOF'\n"
            "#!/bin/bash\n"
            f"head -1 data/part0.csv\n"
            "tail -qn +2 data/*.csv | sort -s -t, -k1,1n\n"
            "EOF\n"
            f"bash {fname} > merged.csv\n"
        ),
    )
