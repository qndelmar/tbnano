"""files_text templates (spec 5.3, ~25%): logs, extraction, line ops.

Each function is one *template*; variants are seeded instances of it.
"""

from __future__ import annotations

import random
from pathlib import Path

from .base import answer_test, files_test, write_task, with_id

LEVELS = ["INFO", "WARN", "ERROR", "DEBUG", "CRITICAL"]
MSGS = ["request handled", "connection opened", "disk check ok", "user login",
        "cache miss", "retry scheduled", "heartbeat", "job started",
        "write complete", "gc pause", "worker spawned", "probe failed"]
LOG_FILES = ["app.log", "server.log", "system.log", "daemon.log", "svc.log"]


def _log(rng, n, target=None, k=0):
    pos = set(rng.sample(range(n), k)) if k else set()
    lines = []
    for i in range(n):
        lvl = target if i in pos else rng.choice([l for l in LEVELS if l != target])
        lines.append(
            f"2024-03-{rng.randint(1,28):02d}T{rng.randint(0,23):02d}:{rng.randint(0,59):02d}:{rng.randint(0,59):02d}Z "
            f"[{lvl}] {rng.choice(MSGS)} #{i}")
    return "\n".join(lines) + "\n"


def log_count(rng, idx, out_root, split):
    fname, tgt = rng.choice(LOG_FILES), rng.choice(["ERROR", "WARN", "CRITICAL"])
    k = rng.randint(5, 40)
    log = _log(rng, rng.randint(80, 200), tgt, k)
    tid = f"logcount-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        f"How many lines in {fname} have level {tgt} (shown as [{tgt}] at the "
        f"start)? Answer with just the number.",
        answer_mode="answer", max_turns=4, tags=["grep", "count"], template="log_count",
        seed=rng.randint(0, 10**6), split=split, setup_files={fname: log},
        test_py=answer_test(float(k), 0.0),
        solution_sh=f"grep -c '\\[{tgt}\\]' {fname} > answer.txt\n")


def log_count_window(rng, idx, out_root, split):
    fname, tgt = rng.choice(LOG_FILES), rng.choice(["ERROR", "WARN"])
    n, k = rng.randint(80, 150), rng.randint(5, 25)
    h1, h2 = sorted(rng.sample(range(0, 22), 2))
    lines, cnt = [], 0
    for i in range(n):
        h = rng.randint(0, 23)
        lvl = rng.choice(LEVELS)
        if lvl == tgt and h1 <= h <= h2:
            cnt += 1
        lines.append(f"2024-03-05T{h:02d}:{rng.randint(0,59):02d}:00Z [{lvl}] msg {i}")
    log = "\n".join(lines) + "\n"
    tid = f"logwin-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "files_text",
        f"In {fname}, count lines with level [{tgt}] whose timestamp hour is "
        f"between {h1:02d} and {h2:02d} inclusive (format T HH:MM:SSZ). "
        f"Answer with just the number.",
        answer_mode="answer", max_turns=6, tags=["grep", "count"], template="log_count_window",
        seed=rng.randint(0, 10**6), split=split, setup_files={fname: log},
        test_py=answer_test(float(cnt), 0.0),
        solution_sh=(f"grep '\\[{tgt}\\]' {fname} | awk -F'T' '{{print $2}}' | "
                     f"cut -d: -f1 | awk '$1>={h1} && $1<={h2}' | wc -l > answer.txt\n"))


def log_first_err(rng, idx, out_root, split):
    fname = rng.choice(LOG_FILES)
    n, k = rng.randint(50, 120), rng.randint(5, 20)
    pos = sorted(rng.sample(range(n), k))
    lines = [f"[{'ERROR' if i in pos else rng.choice(['INFO','WARN','DEBUG'])}] e{i}"
             for i in range(n)]
    tid = f"logfirst-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        f"What is the 1-based line number of the first [ERROR] line in {fname}? "
        f"Answer with just the number.",
        answer_mode="answer", max_turns=4, tags=["grep", "first"], template="log_first_err",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: "\n".join(lines) + "\n"},
        test_py=answer_test(float(pos[0] + 1), 0.0),
        solution_sh=f"grep -n '\\[ERROR\\]' {fname} | head -1 | cut -d: -f1 > answer.txt\n")


def extract_ips(rng, idx, out_root, split):
    # Adapted from TerminalBench 1.0 "analyze-access-logs".
    fname, out = rng.choice(["access.log", "requests.log", "edge.log"]), rng.choice(["ips.txt", "clients.txt"])
    ips = sorted({".".join(str(rng.randint(1, 254)) for _ in range(4))
                  for _ in range(rng.randint(6, 15))})
    lines = []
    for i, ip in enumerate(ips):
        for _ in range(rng.randint(1, 4)):
            lines.append(f'{ip} - - [15/Mar/2024:10:0{i % 6}:{rng.randint(0,59):02d} +0000] "GET /x/{i} HTTP/1.1" {rng.choice([200,301,404,500])} {rng.randint(100,9999)}')
    for _ in range(rng.randint(20, 60)):
        lines.append(f'- - - [15/Mar/2024:11:00:00 +0000] "POST /i/{rng.randint(0,99)} HTTP/1.1" 403 0')
    rng.shuffle(lines)
    tid = f"extractips-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "files_text",
        f"{fname} is a web access log. Extract every client IPv4 address (the "
        f"first token of each request line), deduplicate, sort "
        f"lexicographically, and write them one per line to {out}.",
        answer_mode="files", max_turns=6, tags=["grep", "sort"], template="extract_ips",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: "\n".join(lines) + "\n"},
        test_py=files_test(out, "\n".join(ips) + "\n"),
        solution_sh=f"grep -oE '([0-9]{{1,3}}\\.){{3}}[0-9]{{1,3}}' {fname} | sort -u > {out}\n",
        origin="tb1/analyze-access-logs")


def extract_emails(rng, idx, out_root, split):
    fname, out = "maillog.txt", rng.choice(["emails.txt", "senders.txt"])
    doms = ["a.com", "b.org", "corp.net"]
    mails = sorted({f"{rng.choice(['ops','dev','qa','root','svc'])}{rng.randint(1,99)}@{rng.choice(doms)}"
                    for _ in range(rng.randint(5, 12))})
    lines = []
    for m in mails:
        lines += [f"from=<{m}> size={rng.randint(100,9999)}" for _ in range(rng.randint(1, 3))]
    lines += ["other log line"] * rng.randint(10, 30)
    rng.shuffle(lines)
    tid = f"extmail-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "files_text",
        f"{fname} is a mail log with from=<address> fields. Extract unique "
        f"addresses, sort lexicographically, write one per line to {out}.",
        answer_mode="files", max_turns=6, tags=["grep", "sort"], template="extract_emails",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: "\n".join(lines) + "\n"},
        test_py=files_test(out, "\n".join(mails) + "\n"),
        solution_sh=f"grep -oE 'from=<[^>]+>' {fname} | sed 's/from=<//;s/>//' | sort -u > {out}\n")


def extract_urls(rng, idx, out_root, split):
    fname, out = "crawl.log", "urls.txt"
    urls = sorted({f"/{rng.choice(['api','img','doc','v2'])}/{rng.randint(1,500)}"
                   for _ in range(rng.randint(6, 14))})
    lines = [f'GET {u} HTTP/1.1 {rng.choice([200,404])}' for u in urls for _ in range(rng.randint(1, 3))]
    lines += ["noise line"] * rng.randint(5, 20)
    rng.shuffle(lines)
    tid = f"exturl-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "files_text",
        f"{fname} has GET request lines. Extract unique URL paths, sort, "
        f"write one per line to {out}.",
        answer_mode="files", max_turns=6, tags=["extract"], template="extract_urls",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: "\n".join(lines) + "\n"},
        test_py=files_test(out, "\n".join(urls) + "\n"),
        solution_sh=f"grep -oE 'GET [^ ]+' {fname} | sed 's/^GET //' | sort -u > {out}\n")


def csv_col(rng, idx, out_root, split):
    cols = rng.choice([("name", "score", "team"), ("id", "city", "temp"), ("sku", "qty", "wh")])
    which = rng.randint(0, 2)
    out = rng.choice(["col.txt", "extract.txt"])
    rows = [[f"r{i}", str(rng.randint(1, 999)), f"w{rng.randint(1,9)}"] for i in range(rng.randint(8, 25))]
    content = ",".join(cols) + "\n" + "\n".join(",".join(r) for r in rows) + "\n"
    expected = "\n".join(r[which] for r in rows) + "\n"
    tid = f"csvcol-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        f"data.csv has header '{','.join(cols)}'. Write just the values of "
        f"column '{cols[which]}' (skip the header) to {out}, one per line, "
        f"in original order.",
        answer_mode="files", max_turns=5, tags=["csv", "cut"], template="csv_col",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"data.csv": content}, test_py=files_test(out, expected),
        solution_sh=f"tail -n +2 data.csv | cut -d, -f{which+1} > {out}\n")


def sort_desc(rng, idx, out_root, split):
    vals = [str(rng.randint(-999, 999)) for _ in range(rng.randint(10, 40))]
    out = rng.choice(["sorted.txt", "desc.txt"])
    expected = "\n".join(map(str, sorted(map(int, vals), reverse=True))) + "\n"
    tid = f"sortdesc-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        f"nums.txt has one integer per line. Sort numerically descending "
        f"into {out}.",
        answer_mode="files", max_turns=4, tags=["sort"], template="sort_desc",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"nums.txt": "\n".join(vals) + "\n"},
        test_py=files_test(out, expected),
        solution_sh=f"sort -rn nums.txt > {out}\n")


def upper_lines(rng, idx, out_root, split):
    words = [rng.choice(["alpha", "beta", "gamma", "delta", "echo"]) + str(rng.randint(1, 99))
             for _ in range(rng.randint(6, 20))]
    out = "upper.txt"
    tid = f"upper-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        f"names.txt has one name per line. Uppercase every line into {out} "
        f"(same order).",
        answer_mode="files", max_turns=4, tags=["transform"], template="upper_lines",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"names.txt": "\n".join(words) + "\n"},
        test_py=files_test(out, "\n".join(w.upper() for w in words) + "\n"),
        solution_sh=f"tr 'a-z' 'A-Z' < names.txt > {out}\n")


def dedup_lines(rng, idx, out_root, split):
    uniq = [f"w{rng.randint(100,999)}" for _ in range(rng.randint(6, 12))]
    lines = [w for w in uniq for _ in range(rng.randint(1, 3))]
    rng.shuffle(lines)
    seen, expected_l = set(), []
    for w in lines:
        if w not in seen:
            seen.add(w); expected_l.append(w)
    out = rng.choice(["uniq.txt", "dedup.txt"])
    tid = f"dedup-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "files_text",
        f"dups.txt has repeated lines. Remove duplicates keeping first "
        f"occurrence order; write to {out}.",
        answer_mode="files", max_turns=5, tags=["dedup"], template="dedup_lines",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"dups.txt": "\n".join(lines) + "\n"},
        test_py=files_test(out, "\n".join(expected_l) + "\n"),
        solution_sh=f"awk '!seen[$0]++' dups.txt > {out}\n")


def longest_line(rng, idx, out_root, split):
    lines = [rng.choice(MSGS) * rng.randint(1, 6) for _ in range(rng.randint(10, 30))]
    longest = max(len(l) for l in lines)
    fname = rng.choice(["notes.txt", "blob.txt"])
    tid = f"longline-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        f"{fname} has one sentence per line. How many characters are in the "
        f"longest line? Answer with just the number.",
        answer_mode="answer", max_turns=4, tags=["wc"], template="longest_line",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: "\n".join(lines) + "\n"},
        test_py=answer_test(float(longest), 0.0),
        solution_sh=f"awk '{{if(length($0)>m)m=length($0)}}END{{print m}}' {fname} > answer.txt\n")


def count_regex(rng, idx, out_root, split):
    pat = rng.choice(["timeout", "retry", "null"])
    n, k = rng.randint(60, 140), rng.randint(4, 30)
    pos = set(rng.sample(range(n), k))
    safe = [m for m in MSGS if pat not in m]
    lines = [f"[{rng.choice(LEVELS)}] {'has ' + pat + ' here' if i in pos else 'plain ' + rng.choice(safe)}"
             for i in range(n)]
    fname = rng.choice(LOG_FILES)
    tid = f"regexcount-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "files_text",
        f"How many lines in {fname} contain the word '{pat}'? Answer with "
        f"just the number.",
        answer_mode="answer", max_turns=5, tags=["grep"], template="count_regex",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: "\n".join(lines) + "\n"},
        test_py=answer_test(float(k), 0.0),
        solution_sh=f"grep -cw {pat} {fname} > answer.txt\n")


def merge_logs(rng, idx, out_root, split):
    n = rng.randint(15, 30)
    a = [(f"2024-03-05T{rng.randint(0,23):02d}:{rng.randint(0,59):02d}:00Z", f"A{i}") for i in range(n)]
    b = [(f"2024-03-05T{rng.randint(0,23):02d}:{rng.randint(0,59):02d}:00Z", f"B{i}") for i in range(n)]
    a.sort(); b.sort()
    merged = sorted([f"{t} {m}" for t, m in a + b])
    out = "merged.log"
    tid = f"mergelog-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "files_text",
        f"a.log and b.log are timestamped logs (line starts with ISO "
        f"timestamp). Merge them sorted by timestamp into {out}.",
        answer_mode="files", max_turns=8, tags=["sort", "merge"], template="merge_logs",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"a.log": "\n".join(f"{t} {m}" for t, m in a) + "\n",
                     "b.log": "\n".join(f"{t} {m}" for t, m in b) + "\n"},
        test_py=files_test(out, "\n".join(merged) + "\n"),
        solution_sh=f"sort -k1,1 a.log b.log > {out}\nhead {out}\n")


def jsonl_filter(rng, idx, out_root, split):
    key, want = "kind", rng.choice(["event", "metric", "alarm"])
    rows = [{"kind": rng.choice(["event", "metric", "alarm"]), "v": rng.randint(0, 99)}
            for _ in range(rng.randint(15, 40))]
    keep = [r for r in rows if r[key] == want]
    import json as _j
    out = "out.jsonl"
    tid = f"jsonlf-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "files_text",
        f"in.jsonl has JSON objects per line with a 'kind' field. Keep only "
        f"lines with kind==\"{want}\" verbatim, write to {out} in original "
        f"order.",
        answer_mode="files", max_turns=6, tags=["json", "filter"], template="jsonl_filter",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"in.jsonl": "\n".join(_j.dumps(r) for r in rows) + "\n"},
        test_py=files_test(out, "\n".join(_j.dumps(r) for r in keep) + "\n"),
        solution_sh=f"grep '\"kind\": \"{want}\"' in.jsonl > {out}\n")


def seq_gap(rng, idx, out_root, split):
    start, n = rng.randint(1, 50), rng.randint(30, 80)
    missing = rng.randint(start + 5, start + n - 5)
    ids = [i for i in range(start, start + n) if i != missing]
    fname = "ids.txt"
    tid = f"seqgap-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "files_text",
        f"{fname} has consecutive integer IDs, exactly one missing. Which ID "
        f"is missing? Answer with just the number.",
        answer_mode="answer", max_turns=5, tags=["seq"], template="seq_gap",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: "\n".join(map(str, ids)) + "\n"},
        test_py=answer_test(float(missing), 0.0),
        solution_sh=(f"python3 -c \"v=[int(l) for l in open('{fname}')];"
                     f"print(set(range(v[0],v[-1]+1))-set(v))\" | "
                     f"tr -d '{{}} ' > answer.txt\n"))


def sed_replace(rng, idx, out_root, split):
    old, new = rng.choice(["HOST", "PORT", "MODE"]), rng.choice(["prod", "edge", "v2"])
    fname = "cfg.txt"
    lines = [f"{old}={rng.choice(['dev','old','x'])}" if i % 3 == 0 else f"k{i}=v{i}"
             for i in range(rng.randint(8, 20))]
    out = "cfg_fixed.txt"
    expected = "\n".join(l.replace(f"{old}=", f"{new}=") for l in lines) + "\n"
    tid = f"sedrep-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        f"{fname} uses the old key '{old}='. Write {out} with every "
        f"'{old}=' replaced by '{new}='.",
        answer_mode="files", max_turns=4, tags=["sed"], template="sed_replace",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: "\n".join(lines) + "\n"},
        test_py=files_test(out, expected),
        solution_sh=f"sed 's/^{old}=/{new}=/' {fname} > {out}\n")


# ---------------- train-only templates (disjoint from test) --------------

def t_wc_lines(rng, idx, out_root, split):
    n = rng.randint(50, 200)
    fname = "data.txt"
    tid = f"twclines-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        f"How many lines does {fname} have? Answer with just the number.",
        answer_mode="answer", max_turns=4, tags=["wc"], template="t_wc_lines",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={fname: "\n".join(f"line {i}" for i in range(n)) + "\n"},
        test_py=answer_test(float(n), 0.0), solution_sh=f"wc -l < {fname} > answer.txt\n")


def t_grep_count(rng, idx, out_root, split):
    pat = rng.choice(["ok", "fail", "warn"])
    n, k = rng.randint(40, 120), rng.randint(5, 30)
    pos = set(rng.sample(range(n), k))
    lines = [pat if i in pos else "x" for i in range(n)]
    tid = f"tgrep-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        f"Count lines equal to exactly '{pat}' in list.txt. Answer with just "
        f"the number.",
        answer_mode="answer", max_turns=4, tags=["grep"], template="t_grep_count",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"list.txt": "\n".join(lines) + "\n"},
        test_py=answer_test(float(k), 0.0),
        solution_sh=f"grep -c '^{pat}$' list.txt > answer.txt\n")


def t_sort_alpha(rng, idx, out_root, split):
    words = [f"{rng.choice(['kiwi','plum','fig','oak','elm'])}{rng.randint(1,99)}"
             for _ in range(rng.randint(8, 25))]
    tid = f"tsort-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        "Sort words.txt alphabetically into sorted.txt.",
        answer_mode="files", max_turns=4, tags=["sort"], template="t_sort_alpha",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"words.txt": "\n".join(words) + "\n"},
        test_py=files_test("sorted.txt", "\n".join(sorted(words)) + "\n"),
        solution_sh="sort words.txt > sorted.txt\n")


def t_head_n(rng, idx, out_root, split):
    n, k = rng.randint(30, 80), rng.randint(3, 10)
    lines = [f"L{i}" for i in range(n)]
    tid = f"thead-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        f"Write the first {k} lines of big.txt to top.txt.",
        answer_mode="files", max_turns=4, tags=["head"], template="t_head_n",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"big.txt": "\n".join(lines) + "\n"},
        test_py=files_test("top.txt", "\n".join(lines[:k]) + "\n"),
        solution_sh=f"head -n {k} big.txt > top.txt\n")


def t_tail_n(rng, idx, out_root, split):
    n, k = rng.randint(30, 80), rng.randint(3, 10)
    lines = [f"L{i}" for i in range(n)]
    tid = f"ttail-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        f"Write the last {k} lines of big.txt to bottom.txt.",
        answer_mode="files", max_turns=4, tags=["tail"], template="t_tail_n",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"big.txt": "\n".join(lines) + "\n"},
        test_py=files_test("bottom.txt", "\n".join(lines[-k:]) + "\n"),
        solution_sh=f"tail -n {k} big.txt > bottom.txt\n")


def t_grep_v(rng, idx, out_root, split):
    n, k = rng.randint(40, 100), rng.randint(5, 25)
    pos = set(rng.sample(range(n), k))
    lines = ["DROP" if i in pos else f"keep{i}" for i in range(n)]
    expected = "\n".join(l for l in lines if l != "DROP") + "\n"
    tid = f"tgrepv-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "files_text",
        "Remove every 'DROP' line from list.txt; write the rest to kept.txt "
        "in original order.",
        answer_mode="files", max_turns=5, tags=["grep -v"], template="t_grep_v",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"list.txt": "\n".join(lines) + "\n"},
        test_py=files_test("kept.txt", expected),
        solution_sh="grep -v '^DROP$' list.txt > kept.txt\n")


def t_word_freq(rng, idx, out_root, split):
    w = rng.choice(["cat", "dog", "fox"])
    k = rng.randint(5, 30)
    text = " ".join([w] * k + ["x", "y"] * rng.randint(10, 30))
    tid = f"tfreq-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        f"text.txt has words separated by spaces. How many times does "
        f"'{w}' appear? Answer with just the number.",
        answer_mode="answer", max_turns=4, tags=["count"], template="t_word_freq",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"text.txt": text + "\n"},
        test_py=answer_test(float(k), 0.0),
        solution_sh=f"tr ' ' '\\n' < text.txt | grep -c '^{w}$' > answer.txt\n")


def t_rev_lines(rng, idx, out_root, split):
    lines = [f"r{i}" for i in range(rng.randint(10, 40))]
    tid = f"trev-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        "Reverse the line order of seq.txt into rev.txt.",
        answer_mode="files", max_turns=4, tags=["tac"], template="t_rev_lines",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"seq.txt": "\n".join(lines) + "\n"},
        test_py=files_test("rev.txt", "\n".join(reversed(lines)) + "\n"),
        solution_sh="tac seq.txt > rev.txt\n")


def t_num_sum(rng, idx, out_root, split):
    vals = [rng.randint(1, 999) for _ in range(rng.randint(10, 40))]
    tid = f"tnsum-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        "nums.txt has one integer per line. What is their sum? Answer with "
        "just the number.",
        answer_mode="answer", max_turns=4, tags=["sum"], template="t_num_sum",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"nums.txt": "\n".join(map(str, vals)) + "\n"},
        test_py=answer_test(float(sum(vals)), 0.0),
        solution_sh="awk '{s+=$1}END{print s}' nums.txt > answer.txt\n")


def t_append_line(rng, idx, out_root, split):
    lines = [f"k{i}=v{i}" for i in range(rng.randint(4, 10))]
    add = f"done={rng.randint(100,999)}"
    tid = f"tappend-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "files_text",
        f"Append the line '{add}' to the end of cfg.ini.",
        answer_mode="files", max_turns=4, tags=["append"], template="t_append_line",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"cfg.ini": "\n".join(lines) + "\n"},
        test_py=files_test("cfg.ini", "\n".join(lines) + "\n" + add + "\n"),
        solution_sh=f"echo '{add}' >> cfg.ini\n")
