"""Data family (spec 5.3, ~20%): CSV/JSON filtering and aggregation, sqlite."""

from __future__ import annotations

import random
from pathlib import Path

from .base import answer_test, pick, write_task


def gen_csv_agg(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    # Adapted from TerminalBench 1.0 "bank-trans-filter" (CSV filtering ->
    # a single aggregate answer rather than a pipeline).
    fname = pick(rng, ["metrics.csv", "flights.csv", "sales.csv"],
                 ["ledger.csv", "logbook.csv", "records.csv"], split)
    cat_col, val_col = rng.choice(
        [("region", "revenue"), ("fleet", "duration_s"), ("sensor", "reading")]
    )
    cats = rng.sample(["north", "south", "east", "west", "alpha", "beta", "gamma"], 3)
    rows = []
    for i in range(rng.randint(30, 90)):
        rows.append((i + 1, rng.choice(cats), round(rng.uniform(10, 500), 2)))
    header = f"id,{cat_col},{val_col}"
    content = header + "\n" + "\n".join(f"{a},{b},{c}" for a, b, c in rows) + "\n"
    picked = rng.choice([b for _, b, _ in rows])  # always a present category
    agg = rng.choice(["mean", "sum", "max", "count"])
    vals = [c for _, b, c in rows if b == picked]
    if agg == "mean":
        expected = sum(vals) / len(vals)
        expr = "mean"
    elif agg == "sum":
        expected = sum(vals)
        expr = "total"
    elif agg == "max":
        expected = max(vals)
        expr = "maximum"
    else:
        expected = float(len(vals))
        expr = "number of rows"
    instr = (
        f"In {fname}, compute the {expr} of column '{val_col}' for rows "
        f"where '{cat_col}' is '{picked}'. Answer with just the number."
    )
    sol = (
        f"python3 -c \"\nimport csv\nrows=[r for r in csv.DictReader(open('{fname}'))]\n"
        f"v=[float(r['{val_col}']) for r in rows if r['{cat_col}']=='{picked}']\n"
        f"print({{'mean':sum(v)/len(v),'sum':sum(v),'max':max(v),'count':len(v)}}['{agg}'])\n"
        f"\" > answer.txt\n"
    )
    tid = f"csvagg-{split}-{idx:03d}"
    return write_task(
        out_root, tid, level=2, category="data",
        instruction=instr, answer_mode="answer", max_turns=6,
        tags=["csv", "aggregate"], seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: content},
        test_py=answer_test(expected),
        solution_sh=sol,
        origin="tb1/bank-trans-filter",
    )


def gen_sqlite_q(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    table = pick(rng, ["readings", "events", "telemetry"],
                 ["samples", "measures", "channels"], split)
    col = pick(rng, ["temp", "voltage", "rpm", "pressure"],
               ["current", "freq", "torque", "flow"], split)
    thresh = rng.choice([20, 50, 75, 100, 150])
    n = rng.randint(30, 80)
    vals = [round(rng.uniform(0, 200), 1) for _ in range(n)]
    expected = sum(1 for v in vals if v > thresh)
    # The DB is built at materialisation time so the binary is deterministic
    # given the seed (sqlite file bytes differ per host, so we also commit
    # the generated .sql for transparency).
    inserts = "\n".join(
        f"INSERT INTO {table} (id, {col}) VALUES ({i+1}, {v});"
        for i, v in enumerate(vals)
    )
    setup_sh = f"""\
python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE {table} (id INTEGER PRIMARY KEY, {col} REAL)')
db.executescript('''
{inserts}
''')
db.commit(); db.close()
PY
"""
    instr = (
        f"db.sqlite contains table '{table}' (columns: id, {col}). "
        f"How many rows have {col} greater than {thresh}? "
        f"Answer with just the number."
    )
    sol = (
        f"python3 -c \"import sqlite3;"
        f"print(sqlite3.connect('db.sqlite').execute("
        f"'select count(*) from {table} where {col}>{thresh}').fetchone()[0])\""
        f" > answer.txt\n"
    )
    tid = f"sqliteq-{split}-{idx:03d}"
    return write_task(
        out_root, tid, level=2, category="data",
        instruction=instr, answer_mode="answer", max_turns=6,
        tags=["sqlite", "query"], seed=rng.randint(0, 10**6), split=split,
        setup_files={"seed.sql": f"CREATE TABLE {table} (id INTEGER PRIMARY KEY, {col} REAL);\n{inserts}\n"},
        setup_sh=setup_sh,
        test_py=answer_test(float(expected), rel_tol=0.0),
        solution_sh=sol,
    )


def gen_json_agg(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    fname = pick(rng, ["records.json", "events.json", "inventory.json"],
                 ["items.json", "jobs.json", "fleet.json"], split)
    statuses = rng.sample(["active", "idle", "failed", "retired", "queued"], 3)
    key = pick(rng, ["status", "state", "mode"], ["phase", "kind", "flag"], split)
    recs = [
        {"id": i + 1, key: rng.choice(statuses), "value": round(rng.uniform(1, 100), 2)}
        for i in range(rng.randint(25, 70))
    ]
    picked = rng.choice(statuses)
    agg = rng.choice(["count", "sum"])
    sel = [r["value"] for r in recs if r[key] == picked]
    expected = float(len(sel)) if agg == "count" else sum(sel)
    instr = (
        f"{fname} is a JSON array of objects with keys 'id', '{key}', 'value'. "
        + (f"How many objects have {key} '{picked}'?" if agg == "count"
           else f"Sum 'value' over objects with {key} '{picked}'.")
        + " Answer with just the number."
    )
    import json as _json

    if agg == "count":
        expr = f"sum(1 for r in d if r['{key}']=='{picked}')"
    else:
        expr = f"sum(r['value'] for r in d if r['{key}']=='{picked}')"
    sol = (
        f"python3 -c \"import json;d=json.load(open('{fname}'));"
        f"print({expr})\" > answer.txt\n"
    )
    tid = f"jsonagg-{split}-{idx:03d}"
    return write_task(
        out_root, tid, level=2, category="data",
        instruction=instr, answer_mode="answer", max_turns=6,
        tags=["json", "aggregate"], seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: _json.dumps(recs, indent=1)},
        test_py=answer_test(expected, rel_tol=1e-3 if agg == "sum" else 0.0),
        solution_sh=sol,
    )
