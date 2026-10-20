"""code templates (spec 5.3, ~15%): fix broken scripts, write small tools."""

from __future__ import annotations

from pathlib import Path

from .base import answer_test, files_test, write_task, with_id

# (task writes a check script plus the buggy program; oracle fixes then runs)
PY_BUGS = [
    ("offbyone.py", "xs = [int(x) for x in open('nums.txt')]\n"
     "print(sum(xs[:len(xs)-1]))\n",
     "xs = [int(x) for x in open('nums.txt')]\nprint(sum(xs))\n",
     "drop the -1 so the whole list is summed"),
    ("fact.py", "def f(n):\n    r = 1\n    for i in range(n):\n        r *= i\n    return r\nprint(f(N))\n",
     "def f(n):\n    r = 1\n    for i in range(1, n + 1):\n        r *= i\n    return r\nprint(f(N))\n",
     "range(n) starts at 0; iterate 1..n"),
    ("avg.py", "xs = open('nums.txt').read().split()\ns = 0\nfor x in xs:\n    s += x\nprint(s / len(xs))\n",
     "xs = open('nums.txt').read().split()\ns = 0.0\nfor x in xs:\n    s += float(x)\nprint(s / len(xs))\n",
     "x is a str; convert with float()"),
]


def fix_python(rng, idx, out_root, split):
    # Adapted from TerminalBench 1.0 "fix-code-vulnerability"-style repair tasks.
    name, buggy, fixed, hint = rng.choice(PY_BUGS)
    vals = [rng.randint(1, 50) for _ in range(rng.randint(5, 12))]
    n = rng.randint(3, 8)
    buggy = buggy.replace("N", str(n))
    fixed = fixed.replace("N", str(n))
    files = {name: buggy}
    if "nums.txt" in buggy:
        files["nums.txt"] = "\n".join(map(str, vals)) + "\n"
    import contextlib, io, os, tempfile
    buf = io.StringIO()
    with tempfile.TemporaryDirectory() as td:
        if "nums.txt" in buggy:
            Path(td, "nums.txt").write_text(files["nums.txt"])
        cwd = os.getcwd()
        os.chdir(td)
        try:
            with contextlib.redirect_stdout(buf):
                exec(fixed, {"__name__": "__main__"})
        finally:
            os.chdir(cwd)
    exp_text = buf.getvalue()
    tid = f"fixpy-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "code",
        f"{name} is buggy ({hint}). Fix it so it prints the correct value, "
        f"then write its output to out.txt.",
        answer_mode="files", max_turns=8, tags=["debug", "python"], template="fix_python",
        seed=rng.randint(0, 10**6), split=split, setup_files=files,
        test_py=files_test("out.txt", exp_text),
        solution_sh=f"cat > {name} <<'EOF'\n{fixed}EOF\npython3 {name} > out.txt\ncat out.txt\n")


BASH_BUGS = [
    ('for i in 1 2 3\ndo\n  echo "n=$i"\ndone\n',
     'for i in 1 2 3; do\n  echo "n=$i"\ndone\n', "'do' must be on the 'for' line or after a semicolon"),
    ('x=5\nif [ $x -gt 3 ]\n  echo big\nfi\n',
     'x=5\nif [ $x -gt 3 ]; then\n  echo big\nfi\n', "missing 'then'"),
    ('echo $((1 + 2)\n', 'echo $((1 + 2))\n', "unbalanced arithmetic parens"),
]


def fix_bash(rng, idx, out_root, split):
    buggy, fixed, hint = rng.choice(BASH_BUGS)
    exp_lines = []
    if "n=$i" in fixed:
        exp_lines = ["n=1", "n=2", "n=3"]
    elif "big" in fixed:
        exp_lines = ["big"]
    else:
        exp_lines = ["3"]
    exp = "\n".join(exp_lines) + "\n"
    tid = f"fixsh-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "code",
        f"run.sh fails ({hint}). Fix it and write its stdout to out.txt.",
        answer_mode="files", max_turns=6, tags=["debug", "bash"], template="fix_bash",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"run.sh": buggy},
        test_py=files_test("out.txt", exp),
        solution_sh=f"cat > run.sh <<'EOF'\n{fixed}EOF\nbash run.sh > out.txt\n")


def fix_offbyone(rng, idx, out_root, split):
    n = rng.randint(5, 15)
    prog = (f"for i in range({n}):\n    print(i)\n")
    fixed = f"for i in range(1, {n + 1}):\n    print(i)\n"
    exp = "\n".join(str(i) for i in range(1, n + 1)) + "\n"
    tid = f"offby-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "code",
        f"seq.py prints 0..{n - 1} but must print 1..{n}. Fix it and write "
        f"its output to out.txt.",
        answer_mode="files", max_turns=5, tags=["debug"], template="fix_offbyone",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"seq.py": prog},
        test_py=files_test("out.txt", exp),
        solution_sh=f"cat > seq.py <<'EOF'\n{fixed}EOF\npython3 seq.py > out.txt\n")


def fix_c(rng, idx, out_root, split):
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    buggy = (f'#include <stdio.h>\nint main(){{\n  int x = {a} * {b}\n'
             f'  printf("%d\\n", x);\n  return 0;\n}}\n')
    fixed = buggy.replace(f"int x = {a} * {b}\n", f"int x = {a} * {b};\n")
    tid = f"fixc-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "code",
        "prog.c does not compile (missing semicolon). Fix it, compile with "
        "cc to ./prog, run it, write its output to out.txt.",
        answer_mode="files", max_turns=8, tags=["c", "debug"], template="fix_c",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"prog.c": buggy},
        test_py=files_test("out.txt", f"{a * b}\n"),
        solution_sh=("cat > prog.c <<'EOF'\n" + fixed +
                     "EOF\ncc prog.c -o prog\n./prog > out.txt\ncat out.txt\n"))


def fix_make(rng, idx, out_root, split):
    mk = "all:\n    echo built\n"  # spaces instead of tab
    tid = f"fixmk-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "code",
        "Makefile fails ('missing separator'): the recipe is indented with "
        "spaces. Fix it (tab), run `make`, write its output to out.txt.",
        answer_mode="files", max_turns=8, tags=["make"], template="fix_make",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"Makefile": mk},
        test_py=files_test("out.txt", "echo built\nbuilt\n"),
        solution_sh="printf 'all:\\n\\techo built\\n' > Makefile\nmake > out.txt\n")


def fix_regex(rng, idx, out_root, split):
    buggy = ("import re, sys\n"
             "lines = [l for l in open('in.txt') if re.search(r'[0-9+', l)]\n"
             "print(len(lines))\n")
    fixed = buggy.replace("[0-9+", "[0-9]+")
    k = rng.randint(4, 20)
    n = rng.randint(20, 60)
    pos = set(rng.sample(range(n), k))
    words = ["alpha", "beta", "gamma", "delta"]
    lines = [rng.choice(words) if i not in pos else f"v{i}={rng.randint(10,99)}" for i in range(n)]
    tid = f"fixre-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "code",
        "count.py crashes: the regex '[0-9+' is invalid. Fix it to match "
        "lines containing digits, run it on in.txt, write output to out.txt.",
        answer_mode="files", max_turns=6, tags=["regex"], template="fix_regex",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"count.py": buggy, "in.txt": "\n".join(lines) + "\n"},
        test_py=files_test("out.txt", f"{k}\n"),
        solution_sh=f"sed -i 's/\\[0-9+/[0-9]+/' count.py\npython3 count.py > out.txt\n")


def write_tool(rng, idx, out_root, split):
    n = rng.randint(10, 40)
    lines = [rng.choice(["ok", "fail", "skip"]) for _ in range(n)]
    content = "\n".join(lines) + "\n"
    exp = f"{lines.count('fail')}\n"
    tid = f"wtool-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "code",
        "Write a shell script count.sh that counts lines equal to 'fail' in "
        "results.txt and prints the number. Run it, save output to out.txt.",
        answer_mode="files", max_turns=8, tags=["script"], template="write_tool",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"results.txt": content},
        test_py=_write_tool_test(),
        solution_sh=("cat > count.sh <<'EOF'\ngrep -c '^fail$' results.txt\nEOF\n"
                     "bash count.sh > out.txt\ncat out.txt\n"))


def _write_tool_test():
    return '''\
import os, subprocess
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_file_present():
    assert (BASE / "count.sh").exists(), "count.sh missing"

def test_out():
    assert (BASE / "out.txt").exists(), "out.txt missing"
    exp = subprocess.run(["grep", "-c", "^fail$", str(BASE / "results.txt")],
                         capture_output=True, text=True).stdout
    assert (BASE / "out.txt").read_text() == exp
'''


def merge_csv(rng, idx, out_root, split):
    n = rng.randint(8, 20)
    ids = rng.sample(range(100, 999), n)
    a = "\n".join(f"{i},{rng.randint(1,9)}" for i in ids) + "\n"
    b = "\n".join(f"{i},{rng.randint(10,99)}" for i in ids) + "\n"
    tid = f"mrgcsv-{split}-{idx:03d}"
    a_map = {int(l.split(",")[0]): l.split(",")[1] for l in a.strip().split("\n")}
    b_map = {int(l.split(",")[0]): l.split(",")[1] for l in b.strip().split("\n")}
    exp = "".join(f"{i},{a_map[i]},{b_map[i]}\n" for i in sorted(ids))
    return write_task(
        out_root, tid, 4, "code",
        "Write merge.py that joins a.csv (id,va) and b.csv (id,vb) on id "
        "into merged.csv 'id,va,vb' sorted by id, then run it. Verify "
        "merged.csv row count equals the input count.",
        answer_mode="files", max_turns=12, tags=["write", "csv"], template="merge_csv",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"a.csv": a, "b.csv": b},
        test_py=files_test("merged.csv", exp),
        solution_sh=("cat > merge.py <<'PY'\na={l.split(',')[0]: l.split(',')[1] for l in open('a.csv').read().split()}\n"
                     "b={l.split(',')[0]: l.split(',')[1] for l in open('b.csv').read().split()}\n"
                     "out=['%s,%s,%s' % (k, a[k], b[k]) for k in sorted(a, key=int)]\n"
                     "open('merged.csv','w').write('\\n'.join(out)+'\\n')\nPY\n"
                     "python3 merge.py\nwc -l merged.csv a.csv\n"))


def add_flag(rng, idx, out_root, split):
    prog = ("import sys\nprint(' '.join(sys.argv[1:]))\n")
    tid = f"addflag-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "code",
        "echo.py prints its args. Add a '-u' flag that uppercases the output "
        "(run: python3 echo.py -u hello). Run it with '-u hi there' and "
        "write output to out.txt.",
        answer_mode="files", max_turns=8, tags=["edit"], template="add_flag",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"echo.py": prog},
        test_py=files_test("out.txt", "HI THERE\n"),
        solution_sh=("cat > echo.py <<'PY'\nimport sys\nargs = sys.argv[1:]\n"
                     "if args and args[0] == '-u':\n    print(' '.join(args[1:]).upper())\n"
                     "else:\n    print(' '.join(args))\nPY\n"
                     "python3 echo.py -u hi there > out.txt\n"))


def fix_json_conf(rng, idx, out_root, split):
    good = {"port": rng.randint(1000, 9999), "host": "x", "dbg": False}
    buggy = ('{"port": %d, "host": "x", "dbg": false,}\n' % good["port"])
    tid = f"fixjson-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "code",
        "conf.json fails to parse (trailing comma). Fix it, then write the "
        "value of 'port' to out.txt.",
        answer_mode="files", max_turns=6, tags=["json"], template="fix_json_conf",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"conf.json": buggy},
        test_py=files_test("out.txt", f"{good['port']}\n"),
        solution_sh=("sed -i 's/,}/}/' conf.json\n"
                     "python3 -c \"import json;print(json.load(open('conf.json'))['port'])\" > out.txt\n"))


def fix_ini(rng, idx, out_root, split):
    buggy = "[main\nport = PORT_X\n"
    port = rng.randint(1000, 9999)
    buggy = buggy.replace("PORT_X", str(port))
    tid = f"fixini-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "code",
        "app.ini has a broken section header '[main'. Fix it so "
        "configparser reads it, then write port to out.txt.",
        answer_mode="files", max_turns=6, tags=["ini"], template="fix_ini",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"app.ini": buggy},
        test_py=files_test("out.txt", f"{port}\n"),
        solution_sh=("sed -i 's/\\[main/[main]/' app.ini\n"
                     "python3 -c \"import configparser;c=configparser.ConfigParser();"
                     "c.read('app.ini');print(c['main']['port'])\" > out.txt\n"))


# ---------------- train-only --------------------------------------------

def t_fix_print(rng, idx, out_root, split):
    v = rng.randint(10, 99)
    tid = f"tfixp-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "code",
        "p.py fails: it uses 'print x'. Fix to print(x) and write output to "
        "out.txt.",
        answer_mode="files", max_turns=4, tags=["debug"], template="t_fix_print",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"p.py": f"print {v}\n"},
        test_py=files_test("out.txt", f"{v}\n"),
        solution_sh=f"echo 'print({v})' > p.py\npython3 p.py > out.txt\n")


def t_add_shebang(rng, idx, out_root, split):
    tid = f"tsheb-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "code",
        "s.sh runs with bash but lacks a shebang. Add '#!/bin/bash' as the "
        "first line of s.sh.",
        answer_mode="files", max_turns=4, tags=["edit"], template="t_add_shebang",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"s.sh": "echo hi\n"},
        test_py=files_test("s.sh", "#!/bin/bash\necho hi\n"),
        solution_sh="sed -i '1i #!/bin/bash' s.sh\n")


def t_fix_none(rng, idx, out_root, split):
    v = rng.randint(1, 9)
    buggy = f"x = {v}\nif x > 0:\n    print(x)\nelse\n    print(0)\n"
    tid = f"tfixnone-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "code",
        "f.py has a syntax error (missing colon after else). Fix and write "
        "output to out.txt.",
        answer_mode="files", max_turns=4, tags=["debug"], template="t_fix_none",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"f.py": buggy},
        test_py=files_test("out.txt", f"{v}\n"),
        solution_sh=f"cat > f.py <<'EOF'\nx = {v}\nif x > 0:\n    print(x)\nelse:\n    print(0)\nEOF\npython3 f.py > out.txt\n")


def t_write_echo(rng, idx, out_root, split):
    w = rng.choice(["hello", "ok", "done"])
    tid = f"twecho-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "code",
        f"Create run.sh that prints '{w}' when run with bash. Run it, save "
        f"output to out.txt.",
        answer_mode="files", max_turns=5, tags=["script"], template="t_write_echo",
        seed=rng.randint(0, 10**6), split=split,
        test_py=files_test("out.txt", w + "\n"),
        solution_sh=f"echo 'echo {w}' > run.sh\nbash run.sh > out.txt\n")


def t_fix_range(rng, idx, out_root, split):
    n = rng.randint(3, 8)
    buggy = f"for i in range({n})\n    print(i * i)\n"
    tid = f"tfixrng-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "code",
        "sq.py has a missing colon. Fix it and write its output to out.txt.",
        answer_mode="files", max_turns=4, tags=["debug"], template="t_fix_range",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"sq.py": buggy},
        test_py=files_test("out.txt", "\n".join(str(i * i) for i in range(n)) + "\n"),
        solution_sh=f"cat > sq.py <<'EOF'\nfor i in range({n}):\n    print(i * i)\nEOF\npython3 sq.py > out.txt\n")


def t_rm_blank(rng, idx, out_root, split):
    lines = []
    for i in range(rng.randint(8, 20)):
        lines.append(f"l{i}")
        if rng.random() < 0.4:
            lines.append("")
    content = "\n".join(lines) + "\n"
    expected = "\n".join(l for l in lines if l) + "\n"
    tid = f"trmblk-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "code",
        "in.txt has blank lines. Remove them into clean.txt.",
        answer_mode="files", max_turns=4, tags=["sed"], template="t_rm_blank",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"in.txt": content},
        test_py=files_test("clean.txt", expected),
        solution_sh="grep -v '^$' in.txt > clean.txt\n")


def t_append_text(rng, idx, out_root, split):
    tid = f"tappx-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "code",
        "Append a line 'END' to doc.txt.",
        answer_mode="files", max_turns=4, tags=["append"], template="t_append_text",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"doc.txt": "a\nb\n"},
        test_py=files_test("doc.txt", "a\nb\nEND\n"),
        solution_sh="echo END >> doc.txt\n")
