"""L0 track (spec v2, section 2): 1-2 obvious turns, max_turns 4.

Every test template emits TWO tasks from the same generated data:
  - <slug>-g-*  (track=guided): the instruction names the action/command.
  - <slug>-p-*  (track=plain):  the instruction states only the goal.
Identical setup files and tests; only the instruction differs, so the
guided-vs-plain gap measures whether the model acts without a hint.

Train L0 templates (t_l0_*) cover the same skills under different names so
the template sets stay disjoint.
"""

from __future__ import annotations

import random
from pathlib import Path

from .base import answer_test, files_test, write_task

WORDS = (
    "alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo "
    "lima mike november oscar papa quebec romeo sierra tango uniform victor "
    "whiskey xray yankee zulu cobalt ember fjord glacier harbor ion jet"
).split()


def _pair(rng, out_root, slug, idx, split, template, category, tags,
          guided_instr, plain_instr, setup_files, test_py, solution_sh,
          answer_mode="answer"):
    """Write the guided + plain task pair sharing data and checks."""
    out = []
    for track, instr in (("guided", guided_instr), ("plain", plain_instr)):
        tid = f"{slug}{'g' if track == 'guided' else 'p'}-{split}-{idx:03d}"
        out.append(write_task(
            out_root, tid, 0, category, instr,
            answer_mode=answer_mode, max_turns=4, tags=tags + [f"l0_{track}"],
            template=template, seed=rng.randint(0, 10**6), split=split,
            track=track,
            setup_files=setup_files, test_py=test_py,
            solution_sh=solution_sh))
    return out


def text_answer_test(expected: str) -> str:
    """Exact-match answer test (normalized whitespace/case)."""
    return f'''\
import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
ANSWER_FILE = BASE / ".submission" / "answer.txt"
EXPECTED = {expected!r}

def _read_answer():
    env = os.environ.get("TBNANO_ANSWER")
    if env is not None:
        return env
    if ANSWER_FILE.exists():
        return ANSWER_FILE.read_text()
    return ""

def test_answer_present():
    assert _read_answer().strip() != "", "no answer submitted"

def test_answer_value():
    got = " ".join(_read_answer().split()).strip().lower()
    exp = " ".join(EXPECTED.split()).strip().lower()
    assert got == exp, f"got {{got!r}}, expected {{exp!r}}"
'''


def _wordfile(rng, n=None):
    n = n or rng.randint(4, 12)
    lines = [" ".join(rng.choice(WORDS) for _ in range(rng.randint(2, 5)))
             for _ in range(n)]
    return "\n".join(lines) + "\n"


# ---------------- test templates ------------------------------------------

def l0_line_count(rng, idx, out_root, split):
    data = _wordfile(rng)
    n = data.count("\n")
    return _pair(rng, out_root, "lcnt", idx, split, "l0_line_count", "files_text",
                 ["l0", "wc"],
                 "Run `wc -l data.txt` and answer with just the number.",
                 "How many lines are in data.txt? Answer with just the number.",
                 {"data.txt": data}, answer_test(n, 0.0),
                 "wc -l data.txt | awk '{print $1}' > answer.txt\n")


def l0_first_line(rng, idx, out_root, split):
    data = _wordfile(rng)
    first = data.splitlines()[0]
    return _pair(rng, out_root, "lfirst", idx, split, "l0_first_line", "files_text",
                 ["l0", "head"],
                 "Run `head -1 notes.txt` and answer with just the line.",
                 "What is the first line of notes.txt? Answer with just the line.",
                 {"notes.txt": data}, text_answer_test(first),
                 "head -1 notes.txt > answer.txt\n")


def l0_last_line(rng, idx, out_root, split):
    data = _wordfile(rng)
    last = data.splitlines()[-1]
    return _pair(rng, out_root, "llast", idx, split, "l0_last_line", "files_text",
                 ["l0", "tail"],
                 "Run `tail -1 notes.txt` and answer with just the line.",
                 "What is the last line of notes.txt? Answer with just the line.",
                 {"notes.txt": data}, text_answer_test(last),
                 "tail -1 notes.txt > answer.txt\n")


def l0_has_word(rng, idx, out_root, split):
    data = _wordfile(rng)
    present = rng.random() < 0.5
    if present:
        word = rng.choice(data.split())
    else:
        word = rng.choice(["zzz", "qux", "xyzzy", "plugh"])
    exp = "yes" if present else "no"
    return _pair(rng, out_root, "hword", idx, split, "l0_has_word", "files_text",
                 ["l0", "grep"],
                 f"Run `grep -c '{word}' data.txt`; answer yes if the count "
                 f"is greater than 0, otherwise no.",
                 f"Does data.txt contain the word '{word}'? "
                 f"Answer yes or no.",
                 {"data.txt": data}, text_answer_test(exp),
                 f"grep -qc '{word}' data.txt && echo yes > answer.txt || echo no > answer.txt\n")


def l0_run_script(rng, idx, out_root, split):
    out_val = f"{rng.choice(WORDS)}-{rng.randint(100, 999)}"
    script = f"#!/bin/sh\necho {out_val}\n"
    out = _pair(rng, out_root, "runsh", idx, split, "l0_run_script", "env",
                ["l0", "script"],
                "Run `./hello.sh` and answer with just what it prints.",
                "hello.sh is an executable script. What does it print? "
                "Answer with just its output.",
                {"hello.sh": script}, text_answer_test(out_val),
                "./hello.sh > answer.txt\n")
    for d in out:
        (d / "setup" / "hello.sh").chmod(0o755)
    return out


def l0_cat_sub(rng, idx, out_root, split):
    content = f"{rng.choice(WORDS)} {rng.randint(100,999)} {rng.choice(WORDS)}"
    return _pair(rng, out_root, "catsub", idx, split, "l0_cat_sub", "files_text",
                 ["l0", "find"],
                 "Run `ls` then `cat docs/readme.txt`; answer with the "
                 "file's contents.",
                 "There is a text file somewhere under this directory. "
                 "Answer with its contents.",
                 {"docs/readme.txt": content + "\n"},
                 text_answer_test(content),
                 "ls\ncat docs/readme.txt > answer.txt\n")


def l0_json_key(rng, idx, out_root, split):
    import json as _json
    val = rng.choice(WORDS) + str(rng.randint(10, 99))
    data = _json.dumps({"mode": val, "retries": rng.randint(1, 5)})
    return _pair(rng, out_root, "jkey", idx, split, "l0_json_key", "data",
                 ["l0", "json"],
                 "Run `python3 -c \"import json;print(json.load(open('config.json'))['mode'])\"` "
                 "and answer with just the value.",
                 "What is the value of 'mode' in config.json? Answer with "
                 "just the value.",
                 {"config.json": data}, text_answer_test(val),
                 "python3 -c \"import json;print(json.load(open('config.json'))['mode'])\" > answer.txt\n")


def l0_csv_sum(rng, idx, out_root, split):
    n = rng.randint(5, 10)
    vals = [rng.randint(1, 50) for _ in range(n)]
    csv = "x,y\n" + "".join(f"{i+1},{v}\n" for i, v in enumerate(vals))
    exp = sum(vals)
    return _pair(rng, out_root, "csum", idx, split, "l0_csv_sum", "data",
                 ["l0", "csv"],
                 "Run `awk -F, 'NR>1{s+=$2}END{print s}' vals.csv` and "
                 "answer with just the number.",
                 "vals.csv has rows 'x,y' (header first). Sum the y column. "
                 "Answer with just the number.",
                 {"vals.csv": csv}, answer_test(exp, 0.0),
                 "awk -F, 'NR>1{s+=$2}END{print s}' vals.csv > answer.txt\n")


def l0_rename(rng, idx, out_root, split):
    content = "\n".join(rng.choice(WORDS) for _ in range(rng.randint(3, 8))) + "\n"
    test = files_test("data.done", content) + '''\
def test_old_gone():
    assert not (BASE / "data.log").exists(), "data.log still exists"
'''
    return _pair(rng, out_root, "ren", idx, split, "l0_rename", "env",
                 ["l0", "mv"],
                 "Run `mv data.log data.done`.",
                 "Rename data.log to data.done, keeping its contents.",
                 {"data.log": content}, test,
                 "mv data.log data.done\n",
                 answer_mode="files")


def l0_write_line(rng, idx, out_root, split):
    line = f"{rng.choice(WORDS).upper()}-{rng.randint(100,999)}"
    test = files_test("done.txt", line + "\n")
    return _pair(rng, out_root, "wline", idx, split, "l0_write_line", "env",
                 ["l0", "write"],
                 f"Use write_file to create done.txt containing exactly "
                 f"the line '{line}'.",
                 f"Create a file done.txt containing exactly the line "
                 f"'{line}'.",
                 {}, test,
                 f"printf '%s\\n' '{line}' > done.txt\n",
                 answer_mode="files")


# ---------------- train templates -----------------------------------------

def _tpair(rng, out_root, slug, idx, split, template, *a, **kw):
    return _pair(rng, out_root, slug, idx, split, template, *a, **kw)


def t_l0_grep_line(rng, idx, out_root, split):
    data = _wordfile(rng)
    marker = rng.randrange(len(data.splitlines()))
    lines = data.splitlines()
    lines[marker] = "MARKER " + lines[marker]
    data = "\n".join(lines) + "\n"
    target = lines[marker]
    return _tpair(rng, out_root, "tgln", idx, split, "t_l0_grep_line",
                  "files_text", ["l0", "grep"],
                  "Run `grep MARKER notes.txt` and answer with just the line.",
                  "Which line of notes.txt contains MARKER? Answer with "
                  "just the line.",
                  {"notes.txt": data}, text_answer_test(target),
                  "grep MARKER notes.txt > answer.txt\n")


def t_l0_word_count(rng, idx, out_root, split):
    data = _wordfile(rng)
    n = len(data.split())
    return _tpair(rng, out_root, "twcnt", idx, split, "t_l0_word_count",
                  "files_text", ["l0", "wc"],
                  "Run `wc -w words.txt` and answer with just the number.",
                  "How many words are in words.txt? Answer with just the "
                  "number.",
                  {"words.txt": data}, answer_test(n, 0.0),
                  "wc -w words.txt | awk '{print $1}' > answer.txt\n")


def t_l0_mkdir(rng, idx, out_root, split):
    d = rng.choice(["out", "results", "build"]) + str(rng.randint(1, 99))
    test = f'''\
import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_dir_exists():
    assert (BASE / {d!r}).is_dir(), "{d} missing"
'''
    return _tpair(rng, out_root, "tmkd", idx, split, "t_l0_mkdir",
                  "env", ["l0", "mkdir"],
                  f"Run `mkdir {d}`.",
                  f"Create a directory named {d}.",
                  {}, test, f"mkdir {d}\n", answer_mode="files")


def t_l0_delete(rng, idx, out_root, split):
    content = _wordfile(rng, 3)
    test = '''\
import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_gone():
    assert not (BASE / "junk.tmp").exists(), "junk.tmp still exists"
'''
    return _tpair(rng, out_root, "tdel", idx, split, "t_l0_delete",
                  "env", ["l0", "rm"],
                  "Run `rm junk.tmp`.",
                  "Delete the file junk.tmp.",
                  {"junk.tmp": content}, test, "rm junk.tmp\n",
                  answer_mode="files")


def t_l0_json_num(rng, idx, out_root, split):
    import json as _json
    val = rng.randint(100, 9999)
    data = _json.dumps({"depth": val, "name": rng.choice(WORDS)})
    return _tpair(rng, out_root, "tjnum", idx, split, "t_l0_json_num",
                  "data", ["l0", "json"],
                  "Run `python3 -c \"import json;print(json.load(open('cfg.json'))['depth'])\"` "
                  "and answer with just the number.",
                  "What is the value of 'depth' in cfg.json? Answer with "
                  "just the number.",
                  {"cfg.json": data}, answer_test(val, 0.0),
                  "python3 -c \"import json;print(json.load(open('cfg.json'))['depth'])\" > answer.txt\n")


def t_l0_tsv_sum(rng, idx, out_root, split):
    n = rng.randint(4, 8)
    vals = [rng.randint(1, 40) for _ in range(n)]
    tsv = "a\tb\n" + "".join(f"{i+1}\t{v}\n" for i, v in enumerate(vals))
    exp = sum(vals)
    return _tpair(rng, out_root, "ttsv", idx, split, "t_l0_tsv_sum",
                  "data", ["l0", "tsv"],
                  "Run `awk -F'\\t' 'NR>1{s+=$2}END{print s}' vals.tsv` and "
                  "answer with just the number.",
                  "vals.tsv has rows 'a<TAB>b' (header first). Sum the b "
                  "column. Answer with just the number.",
                  {"vals.tsv": tsv}, answer_test(exp, 0.0),
                  "awk -F'\\t' 'NR>1{s+=$2}END{print s}' vals.tsv > answer.txt\n")


def t_l0_nth_line(rng, idx, out_root, split):
    data = _wordfile(rng)
    lines = data.splitlines()
    k = rng.randrange(len(lines))
    return _tpair(rng, out_root, "tnth", idx, split, "t_l0_nth_line",
                  "files_text", ["l0", "sed"],
                  f"Run `sed -n '{k+1}p' notes.txt` and answer with just "
                  f"the line.",
                  f"What is line {k+1} of notes.txt? Answer with just the "
                  f"line.",
                  {"notes.txt": data}, text_answer_test(lines[k]),
                  f"sed -n '{k+1}p' notes.txt > answer.txt\n")


def t_l0_append(rng, idx, out_root, split):
    content = _wordfile(rng, 4)
    extra = rng.choice(WORDS)
    test = files_test("log.txt", content + extra + "\n")
    return _tpair(rng, out_root, "tapp", idx, split, "t_l0_append",
                  "env", ["l0", "append"],
                  f"Run `echo {extra} >> log.txt`.",
                  f"Append the line '{extra}' to the end of log.txt.",
                  {"log.txt": content}, test,
                  f"echo {extra} >> log.txt\n", answer_mode="files")
