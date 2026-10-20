"""data templates (spec 5.3, ~20%): csv/tsv/json/jsonl/sqlite."""

from __future__ import annotations

import json as _j
import sqlite3
from pathlib import Path

from .base import answer_test, files_test, kv_test, write_task, with_id


def csv_agg(rng, idx, out_root, split):
    op, col_name = rng.choice([("sum", "qty"), ("avg", "price"), ("count", "id")])
    n = rng.randint(15, 60)
    qtys = [rng.randint(1, 500) for _ in range(n)]
    prices = [rng.randint(1, 200) for _ in range(n)]
    tags = [rng.choice(["x", "y", "z"]) for _ in range(n)]
    content = "id,qty,price,tag\n" + "\n".join(
        f"{i},{q},{p},{t}" for i, (q, p, t) in enumerate(zip(qtys, prices, tags))) + "\n"
    vals = {"qty": qtys, "price": prices, "id": list(range(n))}[col_name]
    exp = {"sum": float(sum(vals)), "avg": sum(vals) / len(vals),
           "count": float(len(vals))}[op]
    tid = f"csvagg-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "data",
        f"sales.csv has columns id,qty,price,tag. What is the {op} of column "
        f"{col_name}? Answer with just the number.",
        answer_mode="answer", max_turns=6, tags=["csv", "agg"], template="csv_agg",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"sales.csv": content}, test_py=answer_test(exp),
        solution_sh=("python3 - <<'PY' > answer.txt\nimport csv\n"
                     "r=list(csv.DictReader(open('sales.csv')))\n"
                     f"v=[float(x['{col_name}']) for x in r]\n"
                     f"print({{'sum':sum(v),'avg':sum(v)/len(v),'count':len(v)}}['{op}'])\nPY\n"))


def csv_topn(rng, idx, out_root, split):
    n, k = rng.randint(15, 50), rng.randint(3, 7)
    vals = rng.sample(range(1, 1000), n)
    rows = [f"item{i},{v}" for i, v in enumerate(vals)]
    exp = float(sum(sorted(vals, reverse=True)[:k]))
    tid = f"csvtopn-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "data",
        f"items.csv has rows 'name,value'. What is the sum of the top {k} "
        f"values? Answer with just the number.",
        answer_mode="answer", max_turns=6, tags=["csv", "topn"], template="csv_topn",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"items.csv": "\n".join(rows) + "\n"},
        test_py=answer_test(exp, 0.0),
        solution_sh=f"cut -d, -f2 items.csv | sort -rn | head -{k} | "
                    f"awk '{{s+=$1}}END{{print s}}' > answer.txt\n")


def csv_join(rng, idx, out_root, split):
    n = rng.randint(8, 25)
    ids = rng.sample(range(100, 999), n)
    a = {i: f"u{rng.randint(10,99)}" for i in ids}
    b = {i: rng.randint(1, 50) for i in ids}
    exp = "".join(f"{i},{a[i]},{b[i]}\n" for i in sorted(ids))
    tid = f"csvjoin-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "data",
        "users.csv (id,name) and orders.csv (id,amount) share the id column. "
        "Join them into joined.csv with lines 'id,name,amount' sorted by id.",
        answer_mode="files", max_turns=8, tags=["csv", "join"], template="csv_join",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"users.csv": "\n".join(f"{i},{a[i]}" for i in sorted(ids)) + "\n",
                     "orders.csv": "\n".join(f"{i},{b[i]}" for i in sorted(ids)) + "\n"},
        test_py=files_test("joined.csv", exp),
        solution_sh=("sort -t, -k1,1 users.csv > /tmp/u; sort -t, -k1,1 orders.csv > /tmp/o; "
                     "join -t, /tmp/u /tmp/o > joined.csv\nhead joined.csv\n"))


def sqlite_count(rng, idx, out_root, split):
    g = rng.choice(["a", "b"])
    n = rng.randint(20, 60)
    vals = [(i, rng.randint(1, 9), rng.choice(["a", "b"])) for i in range(n)]
    cnt = sum(1 for v in vals if v[2] == g)
    setup_sh = ("python3 - <<'PY'\nimport sqlite3\ndb = sqlite3.connect('data.db')\n"
                "db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER, g TEXT);')\n"
                f"db.executemany('INSERT INTO t VALUES(?,?,?)', {vals!r})\n"
                "db.commit()\nPY\n")
    tid = f"sqlcount-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "data",
        f"data.db has table t(id, v, g). How many rows have g='{g}'? Answer "
        f"with just the number.",
        answer_mode="answer", max_turns=6, tags=["sqlite"], template="sqlite_count",
        seed=rng.randint(0, 10**6), split=split, setup_sh=setup_sh,
        test_py=answer_test(float(cnt), 0.0),
        solution_sh=f"sqlite3 data.db \"SELECT count(*) FROM t WHERE g='{g}'\" > answer.txt "
                    f"|| python3 -c \"import sqlite3;print(sqlite3.connect('data.db')"
                    f".execute(\\\"SELECT count(*) FROM t WHERE g='{g}'\\\").fetchone()[0])\" > answer.txt\n")


def sqlite_join(rng, idx, out_root, split):
    n = rng.randint(10, 30)
    vals = [(i, rng.randint(1, 99)) for i in range(n)]
    names = [(i, f"n{i}") for i in range(n)]
    keep = sorted(rng.sample(range(n), rng.randint(4, n // 2)))
    exp = float(sum(v for i, v in vals if i in keep))
    inb = set(keep)
    setup_sh = ("python3 - <<'PY'\nimport sqlite3\ndb = sqlite3.connect('data.db')\n"
                "db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER);"
                "CREATE TABLE keep(id INTEGER);')\n"
                f"db.executemany('INSERT INTO t VALUES(?,?)', {vals!r})\n"
                f"db.executemany('INSERT INTO keep VALUES(?)', [(i,) for i in {keep!r}])\n"
                "db.commit()\nPY\n")
    tid = f"sqljoin-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "data",
        "data.db has tables t(id, v) and keep(id). Sum t.v for ids present "
        "in keep. Answer with just the number.",
        answer_mode="answer", max_turns=8, tags=["sqlite", "join"], template="sqlite_join",
        seed=rng.randint(0, 10**6), split=split, setup_sh=setup_sh,
        test_py=answer_test(exp, 0.0),
        solution_sh=("python3 -c \"import sqlite3;print(sqlite3.connect('data.db')"
                     ".execute('select name from sqlite_master').fetchall())\"\n"
                     "python3 -c \"import sqlite3;print(sqlite3.connect('data.db')"
                     ".execute('SELECT sum(t.v) FROM t JOIN keep ON t.id=keep.id')"
                     ".fetchone()[0])\" > answer.txt\ncat answer.txt\n"))


def json_agg(rng, idx, out_root, split):
    key = rng.choice(["score", "temp", "watt"])
    rows = [{key: rng.randint(1, 400), "on": rng.choice([True, False])}
            for _ in range(rng.randint(15, 50))]
    exp = float(sum(r[key] for r in rows if r["on"]))
    tid = f"jsonagg-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "data",
        f"metrics.json is a JSON array of objects with '{key}' and 'on' "
        f"fields. Sum {key} where on is true. Answer with just the number.",
        answer_mode="answer", max_turns=6, tags=["json"], template="json_agg",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"metrics.json": _j.dumps(rows)},
        test_py=answer_test(exp),
        solution_sh=f"python3 -c \"import json;d=json.load(open('metrics.json'));"
                    f"print(sum(x['{key}'] for x in d if x['on']))\" > answer.txt\n")


def json_to_csv(rng, idx, out_root, split):
    n = rng.randint(8, 30)
    rows = [{"id": i, "v": rng.randint(1, 99)} for i in range(n)]
    exp = "id,v\n" + "\n".join(f"{r['id']},{r['v']}" for r in rows) + "\n"
    tid = f"jsoncsv-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "data",
        "records.json is a JSON array of {id, v} objects. Convert to "
        "out.csv with header 'id,v' in the same order.",
        answer_mode="files", max_turns=6, tags=["json", "csv"], template="json_to_csv",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"records.json": _j.dumps(rows)},
        test_py=files_test("out.csv", exp),
        solution_sh=("python3 -c \"import json;d=json.load(open('records.json'));"
                     "print('id,v');[print(f\\\"{x['id']},{x['v']}\\\") for x in d]\" "
                     "> out.csv\nhead out.csv\n"))


def csv_stats(rng, idx, out_root, split):
    vals = [rng.randint(10, 500) for _ in range(rng.randint(20, 60))]
    exp = {"min": float(min(vals)), "max": float(max(vals)),
           "sum": float(sum(vals))}
    tid = f"csvstats-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "data",
        "data.csv has one number per line. Write stats.txt with lines "
        "'min=<v>', 'max=<v>', 'sum=<v>' in that order.",
        answer_mode="files", max_turns=8, tags=["csv", "stats"], template="csv_stats",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"data.csv": "\n".join(map(str, vals)) + "\n"},
        test_py=kv_test("stats.txt", exp, 1e-9),
        solution_sh=("python3 -c \"v=[float(l) for l in open('data.csv')];"
                     "open('stats.txt','w').write(f'min={min(v)}\\nmax={max(v)}\\nsum={sum(v)}\\n')\"\n"
                     "cat stats.txt\n"))


def dedup_latest(rng, idx, out_root, split):
    ids = rng.sample(range(100, 999), rng.randint(8, 15))
    rows = []
    for i in ids:
        for _ in range(rng.randint(1, 3)):
            rows.append({"id": i, "ts": rng.randint(1000, 9999), "v": rng.randint(1, 99)})
    rng.shuffle(rows)
    latest = {}
    for r in rows:
        if r["id"] not in latest or r["ts"] > latest[r["id"]]["ts"]:
            latest[r["id"]] = r
    exp = _j.dumps(sorted(latest.values(), key=lambda r: r["id"]))
    tid = f"deduplt-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "data",
        "events.json is a JSON array of {id, ts, v} with duplicate ids. "
        "Keep only the row with max ts per id, sorted by id, write a JSON "
        "array to out.json.",
        answer_mode="files", max_turns=8, tags=["json", "dedup"], template="dedup_latest",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"events.json": _j.dumps(rows)},
        test_py=files_test("out.json", exp),
        solution_sh=("python3 -c 'import json;print(len(json.load(open(\"events.json\"))))'\n"
                     "python3 - <<'PY'\nimport json\nrows=json.load(open('events.json'))\n"
                     "latest={}\nfor r in rows:\n    if r['id'] not in latest or r['ts']>latest[r['id']]['ts']:\n"
                     "        latest[r['id']]=r\n"
                     "out=sorted(latest.values(), key=lambda r: r['id'])\n"
                     "open('out.json','w').write(json.dumps(out))\nPY\n"))


def json_nested(rng, idx, out_root, split):
    n = rng.randint(10, 30)
    rows = [{"id": i, "meta": {"score": rng.randint(1, 99)}} for i in range(n)]
    exp = float(sum(r["meta"]["score"] for r in rows if r["id"] % 2 == 0))
    tid = f"jsonnest-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "data",
        "nest.json is a JSON array of objects {id, meta:{score}}. Sum "
        "meta.score over objects with even id. Answer with just the number.",
        answer_mode="answer", max_turns=8, tags=["json", "nested"], template="json_nested",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"nest.json": _j.dumps(rows)},
        test_py=answer_test(exp),
        solution_sh=("python3 -c 'import json;print(json.load(open(\"nest.json\"))[0])'\n"
                     "python3 -c \"import json;d=json.load(open('nest.json'));"
                     "print(sum(x['meta']['score'] for x in d if x['id']%2==0))\" > answer.txt\ncat answer.txt\n"))


def tsv_to_json(rng, idx, out_root, split):
    n = rng.randint(8, 25)
    rows = [{"id": i, "name": f"n{i}"} for i in range(n)]
    tsv = "id\tname\n" + "\n".join(f"{r['id']}\t{r['name']}" for r in rows) + "\n"
    exp = _j.dumps(rows)
    tid = f"tsvjson-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "data",
        "in.tsv is tab-separated with header 'id\\tname'. Convert to a JSON "
        "array of {id:int, name:str} in out.json (same order).",
        answer_mode="files", max_turns=5, tags=["tsv", "json"], template="tsv_to_json",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"in.tsv": tsv},
        test_py=files_test("out.json", exp),
        solution_sh=("python3 - <<'PY'\nimport csv, json\n"
                     "rows=list(csv.DictReader(open('in.tsv'), delimiter='\\t'))\n"
                     "out=[{'id': int(r['id']), 'name': r['name']} for r in rows]\n"
                     "open('out.json','w').write(json.dumps(out))\nPY\n"))


# ---------------- train-only --------------------------------------------

def t_csv_sum(rng, idx, out_root, split):
    vals = [rng.randint(1, 99) for _ in range(rng.randint(10, 40))]
    content = "v\n" + "\n".join(map(str, vals)) + "\n"
    tid = f"tcsvsum-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "data",
        "data.csv has header 'v' then numbers. Sum them. Answer with just "
        "the number.",
        answer_mode="answer", max_turns=4, tags=["csv"], template="t_csv_sum",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"data.csv": content}, test_py=answer_test(float(sum(vals)), 0.0),
        solution_sh="tail -n +2 data.csv | awk '{s+=$1}END{print s}' > answer.txt\n")


def t_json_count(rng, idx, out_root, split):
    n = rng.randint(10, 60)
    tid = f"tjsoncnt-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "data",
        "list.json is a JSON array. How many elements? Answer with just the "
        "number.",
        answer_mode="answer", max_turns=4, tags=["json"], template="t_json_count",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"list.json": _j.dumps(list(range(n)))},
        test_py=answer_test(float(n), 0.0),
        solution_sh="python3 -c \"import json;print(len(json.load(open('list.json'))))\" > answer.txt\n")


def t_csv_reverse(rng, idx, out_root, split):
    rows = [f"a{i},{rng.randint(1,99)}" for i in range(rng.randint(8, 20))]
    tid = f"tcsvrev-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "data",
        "pairs.csv is 'key,val' rows. Write rev.csv with rows 'val,key' "
        "(swap columns).",
        answer_mode="files", max_turns=4, tags=["csv"], template="t_csv_reverse",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"pairs.csv": "\n".join(rows) + "\n"},
        test_py=files_test("rev.csv",
                           "\n".join(",".join(r.split(",")[::-1]) for r in rows) + "\n"),
        solution_sh="awk -F, '{print $2\",\"$1}' pairs.csv > rev.csv\n")


def t_sql_minmax(rng, idx, out_root, split):
    vals = [(i, rng.randint(1, 999)) for i in range(rng.randint(15, 50))]
    exp = float(max(v for _, v in vals))
    setup_sh = ("python3 - <<'PY'\nimport sqlite3\ndb = sqlite3.connect('m.db')\n"
                "db.execute('CREATE TABLE t(id INTEGER, v INTEGER)')\n"
                f"db.executemany('INSERT INTO t VALUES(?,?)', {vals!r})\n"
                "db.commit()\nPY\n")
    tid = f"tsqlmm-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "data",
        "m.db has table t(id, v). What is max(v)? Answer with just the "
        "number.",
        answer_mode="answer", max_turns=5, tags=["sqlite"], template="t_sql_minmax",
        seed=rng.randint(0, 10**6), split=split, setup_sh=setup_sh,
        test_py=answer_test(exp, 0.0),
        solution_sh="python3 -c \"import sqlite3;print(sqlite3.connect('m.db').execute('SELECT max(v) FROM t').fetchone()[0])\" > answer.txt\n")


def t_json_keys(rng, idx, out_root, split):
    keys = sorted(rng.sample(["alpha", "beta", "gamma", "delta", "eps", "zeta"], rng.randint(3, 5)))
    tid = f"tjsonkeys-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "data",
        "conf.json is a flat JSON object. Write its keys sorted, one per "
        "line, to keys.txt.",
        answer_mode="files", max_turns=4, tags=["json"], template="t_json_keys",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"conf.json": _j.dumps({k: 1 for k in keys})},
        test_py=files_test("keys.txt", "\n".join(keys) + "\n"),
        solution_sh="python3 -c \"import json;print('\\n'.join(sorted(json.load(open('conf.json')))))\" > keys.txt\n")


def t_csv_swap(rng, idx, out_root, split):
    rows = [f"k{i},v{i}" for i in range(rng.randint(5, 15))]
    tid = f"tcsvswap-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "data",
        "m.csv is 'k,v'. Write swapped.csv as 'v,k'.",
        answer_mode="files", max_turns=4, tags=["csv"], template="t_csv_swap",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"m.csv": "\n".join(rows) + "\n"},
        test_py=files_test("swapped.csv",
                           "\n".join(",".join(r.split(",")[::-1]) for r in rows) + "\n"),
        solution_sh="awk -F, '{print $2\",\"$1}' m.csv > swapped.csv\n")


def t_csv_head_filter(rng, idx, out_root, split):
    n, k = rng.randint(20, 50), rng.randint(5, 12)
    rows = [f"{i},{rng.randint(1,99)}" for i in range(n)]
    tid = f"tcvhf-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "data",
        f"t.csv has 'id,val' rows (no header). Write the first {k} rows to "
        f"head.csv.",
        answer_mode="files", max_turns=4, tags=["csv"], template="t_csv_head_filter",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"t.csv": "\n".join(rows) + "\n"},
        test_py=files_test("head.csv", "\n".join(rows[:k]) + "\n"),
        solution_sh=f"head -{k} t.csv > head.csv\n")


def t_tsv_count(rng, idx, out_root, split):
    n = rng.randint(10, 60)
    tid = f"ttsvcnt-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "data",
        "in.tsv has tab-separated rows (no header). How many rows? Answer "
        "with just the number.",
        answer_mode="answer", max_turns=4, tags=["tsv"], template="t_tsv_count",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"in.tsv": "\n".join(f"{i}\tx" for i in range(n)) + "\n"},
        test_py=answer_test(float(n), 0.0),
        solution_sh="wc -l < in.tsv > answer.txt\n")
