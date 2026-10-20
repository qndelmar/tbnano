"""Files & text family (spec 5.3, ~25%): grep/sed/awk/find/sort/jq-ish."""

from __future__ import annotations

import random
from pathlib import Path

from .base import answer_test, pick, write_task

LEVELS = ["INFO", "WARN", "ERROR", "DEBUG", "CRITICAL"]
LOG_FILES_TEST = ["app.log", "server.log", "system.log", "daemon.log"]
LOG_FILES_TRAIN = ["prod.log", "web.log", "audit.log", "core.log"]
MSGS = [
    "request handled", "connection opened", "disk check ok", "user login",
    "cache miss", "retry scheduled", "heartbeat", "job started",
    "write complete", "gc pause", "worker spawned", "probe failed",
]


def gen_log_count(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    fname = pick(rng, LOG_FILES_TEST, LOG_FILES_TRAIN, split)
    target = rng.choice(["ERROR", "WARN", "CRITICAL"])
    n_lines = rng.randint(80, 200)
    k = rng.randint(5, 40)
    positions = set(rng.sample(range(n_lines), k))
    lines = []
    for i in range(n_lines):
        lvl = target if i in positions else rng.choice(
            [l for l in LEVELS if l != target]
        )
        msg = rng.choice(MSGS)
        lines.append(f"2024-03-{rng.randint(1,28):02d}T{rng.randint(0,23):02d}:{rng.randint(0,59):02d}:{rng.randint(0,59):02d}Z [{lvl}] {msg} #{i}")
    log = "\n".join(lines) + "\n"
    tid = f"logcount-{split}-{idx:03d}"
    return write_task(
        out_root, tid,
        level=1, category="files_text",
        instruction=(
            f"How many lines in {fname} have level {target} (shown as "
            f"[{target}] at the start)? Answer with just the number."
        ),
        answer_mode="answer", max_turns=4,
        tags=["grep", "count", "logs"],
        seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: log},
        test_py=answer_test(float(k), rel_tol=0.0),
        solution_sh=f"grep -c '\\[{target}\\]' {fname} > answer.txt\n",
    )


def gen_extract_ips(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    # Adapted from TerminalBench 1.0 "analyze-access-logs" (compressed to a
    # single extraction step so it fits small-model budgets).
    fname = pick(rng, ["access.log", "requests.log", "edge.log"],
                 ["traffic.log", "hits.log", "frontend.log"], split)
    out = pick(rng, ["ips.txt", "clients.txt"], ["addrs.txt", "sources.txt"], split)
    n_ips = rng.randint(6, 15)
    ips = sorted({
        ".".join(str(rng.randint(1, 254)) for _ in range(4))
        for _ in range(n_ips)
    })
    noise_ips = set()
    lines = []
    for i, ip in enumerate(ips):
        for _ in range(rng.randint(1, 4)):
            lines.append(
                f'{ip} - - [15/Mar/2024:10:{rng.randint(0,59):02d}:{rng.randint(0,59):02d} +0000] '
                f'"GET /{rng.choice(["api","static","img","v1"])}/{i} HTTP/1.1" '
                f'{rng.choice([200,200,301,404,500])} {rng.randint(100,9999)}'
            )
    for _ in range(rng.randint(20, 60)):
        lines.append(
            f'- - - [15/Mar/2024:11:{rng.randint(0,59):02d}:{rng.randint(0,59):02d} +0000] '
            f'"POST /internal/{rng.randint(0,99)} HTTP/1.1" {rng.choice([200,403])} 0'
        )
    rng.shuffle(lines)
    log = "\n".join(lines) + "\n"
    expected = "\n".join(ips) + "\n"
    tid = f"extractips-{split}-{idx:03d}"
    return write_task(
        out_root, tid,
        level=2, category="files_text",
        instruction=(
            f"{fname} is a web access log. Extract every client IPv4 "
            f"address (the first token of each request line), deduplicate, "
            f"sort lexicographically, and write them one per line to {out}."
        ),
        answer_mode="files", max_turns=6,
        tags=["grep", "sort", "logs"],
        seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: log},
        test_py=f'''\
import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = {ips!r}

def test_ips_file():
    p = BASE / "{out}"
    assert p.exists(), "{out} missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {{got}}"
''',
        solution_sh=(
            f"grep -oE '([0-9]{{1,3}}\\.){{3}}[0-9]{{1,3}}' {fname} "
            f"| sort -u > {out}\n"
        ),
        origin="tb1/analyze-access-logs",
    )


def gen_field_transform(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    variant = rng.choice(["csv_col", "sort_desc", "uppercase", "dedup"])
    if variant == "csv_col":
        fname = pick(rng, ["data.csv"], ["table.csv"], split)
        col = rng.randint(2, 4)
        ncols = rng.randint(col, col + 2)
        header = [f"c{i}" for i in range(1, ncols + 1)]
        rows = [[str(rng.randint(0, 999)) for _ in range(ncols)] for _ in range(rng.randint(10, 40))]
        content = ",".join(header) + "\n" + "\n".join(",".join(r) for r in rows) + "\n"
        expected = "".join(r[col - 1] + "\n" for r in rows)
        instr = (
            f"{fname} is a CSV with header. Write the values of column "
            f"'{header[col-1]}' (one per line, in order, no header) to col.txt."
        )
        sol = f"tail -n +2 {fname} | cut -d, -f{col} > col.txt\n"
        out = "col.txt"
    elif variant == "sort_desc":
        fname = pick(rng, ["nums.txt"], ["values.txt"], split)
        nums = [rng.randint(-999, 999) for _ in range(rng.randint(15, 60))]
        content = "\n".join(map(str, nums)) + "\n"
        expected = "".join(str(n) + "\n" for n in sorted(nums, reverse=True))
        instr = (
            f"Sort the numbers in {fname} in descending numeric order and "
            f"write the result to sorted.txt (one number per line)."
        )
        sol = f"sort -rn {fname} > sorted.txt\n"
        out = "sorted.txt"
    elif variant == "uppercase":
        fname = pick(rng, ["names.txt"], ["labels.txt"], split)
        names = [rng.choice(["alpha","bravo","charlie","delta","echo","foxtrot","golf"]) + str(i) for i in range(rng.randint(8, 30))]
        content = "\n".join(names) + "\n"
        expected = "".join(n.upper() + "\n" for n in names)
        instr = f"Convert every line of {fname} to uppercase and write the result to up.txt."
        sol = f"tr 'a-z' 'A-Z' < {fname} > up.txt\n"
        out = "up.txt"
    else:
        fname = pick(rng, ["dups.txt"], ["words.txt"], split)
        base = [rng.choice(["red","green","blue","cyan","magenta"]) for _ in range(rng.randint(20, 60))]
        content = "\n".join(base) + "\n"
        expected = "".join(s + "\n" for s in sorted(set(base)))
        instr = (
            f"{fname} has one word per line with duplicates. Write the "
            f"unique words sorted alphabetically to uniq.txt."
        )
        sol = f"sort -u {fname} > uniq.txt\n"
        out = "uniq.txt"

    tid = f"fieldtx-{split}-{idx:03d}"
    return write_task(
        out_root, tid,
        level=2, category="files_text",
        instruction=instr,
        answer_mode="files", max_turns=6,
        tags=["text", "transform"],
        seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: content},
        test_py=f'''\
import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = {expected!r}

def test_output_file():
    p = BASE / "{out}"
    assert p.exists(), "{out} missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
''',
        solution_sh=sol,
    )
