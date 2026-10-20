"""env templates (spec 5.3, ~10%): permissions, paths, git, symlinks."""

from __future__ import annotations

from pathlib import Path

from .base import answer_test, files_test, write_task, with_id


def chmod_run(rng, idx, out_root, split):
    # Adapted from TerminalBench 1.0 "sanitize-git-repo"-adjacent env repair.
    out_v = rng.choice(["ok1", "ok2", "ok3"])
    prog = f"#!/bin/sh\necho {out_v}\n"
    setup_sh = "chmod 0644 tool.sh\n"
    tid = f"chmodx-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "env",
        "tool.sh must be run as ./tool.sh but is not executable. Make it "
        "executable, run it, write output to out.txt.",
        answer_mode="files", max_turns=5, tags=["chmod"], template="chmod_run",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"tool.sh": prog}, setup_sh=setup_sh,
        test_py=files_test("out.txt", out_v + "\n"),
        solution_sh="chmod +x tool.sh\n./tool.sh > out.txt\n")


def misplaced_conf(rng, idx, out_root, split):
    key = rng.choice(["token", "port", "mode"])
    val = str(rng.randint(1000, 9999)) if key == "port" else rng.choice(["a1", "b2", "on"])
    prog = ("import os\nfrom pathlib import Path\n"
            "p = Path('conf/settings.ini')\n"
            "v = [l.split('=',1)[1].strip() for l in p.read_text().splitlines() "
            f"if l.startswith('{key}=')][0]\nprint(v)\n")
    setup_sh = "mkdir -p conf\n"
    tid = f"misconf-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "env",
        "app.py reads conf/settings.ini but the file is at "
        "settings.ini.bak in the task dir. Put it in place, run app.py, "
        "write output to out.txt.",
        answer_mode="files", max_turns=6, tags=["mv"], template="misplaced_conf",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"app.py": prog, "settings.ini.bak": f"{key}={val}\n"},
        setup_sh=setup_sh,
        test_py=files_test("out.txt", val + "\n"),
        solution_sh="mv settings.ini.bak conf/settings.ini\npython3 app.py > out.txt\n")


def missing_dir(rng, idx, out_root, split):
    prog = ("from pathlib import Path\n"
            "Path('out/').mkdir(exist_ok=True)\n"
            "Path('out/done.txt').write_text('done\\n')\nprint('ok')\n")
    tid = f"mkd-{split}-{idx:03d}"
    # actually: script fails because parent 'out' missing? mkdir handles it.
    # real bug: writes to logs/app.log where logs/ missing
    prog = ("open('logs/app.log', 'a').write('start\\n')\nprint('ok')\n")
    return write_task(
        out_root, tid, 2, "env",
        "app.py crashes because directory logs/ does not exist. Create it, "
        "run app.py, write output to out.txt.",
        answer_mode="files", max_turns=6, tags=["mkdir"], template="missing_dir",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"app.py": prog},
        test_py=files_test("out.txt", "ok\n"),
        solution_sh="mkdir -p logs\npython3 app.py > out.txt\n")


def git_restore(rng, idx, out_root, split):
    v = rng.randint(10, 99)
    setup_sh = (
        "git init -q . && git config user.email t@t && git config user.name t\n"
        f"printf 'x={v}\\n' > cfg.txt && git add cfg.txt && git commit -qm init\n"
        "printf 'x=BROKEN\\n' > cfg.txt\n")
    tid = f"gitrest-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "env",
        "cfg.txt was overwritten with 'x=BROKEN'. Restore the committed "
        "version (git), then write the value of x to out.txt.",
        answer_mode="files", max_turns=8, tags=["git"], template="git_restore",
        seed=rng.randint(0, 10**6), split=split, setup_sh=setup_sh,
        test_py=files_test("out.txt", f"{v}\n"),
        solution_sh="git status\ngit checkout -- cfg.txt\ncut -d= -f2 cfg.txt > out.txt\n")


def symlink_fix(rng, idx, out_root, split):
    data = f"payload-{rng.randint(10,99)}\n"
    setup_sh = "ln -sf missing.txt link.txt\n"
    tid = f"symfix-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "env",
        "link.txt is a dangling symlink (points to missing.txt). Real data "
        "is in data.txt. Repoint link.txt at data.txt, then copy the "
        "resolved content to out.txt.",
        answer_mode="files", max_turns=6, tags=["ln"], template="symlink_fix",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"data.txt": data}, setup_sh=setup_sh,
        test_py=files_test("out.txt", data),
        solution_sh="ls -l link.txt\nln -sf data.txt link.txt\ncat link.txt > out.txt\n")


def git_diff_stat(rng, idx, out_root, split):
    a = rng.randint(2, 10)
    b = rng.randint(2, 10)
    setup_sh = (
        "git init -q . && git config user.email t@t && git config user.name t\n"
        "seq 1 20 > f.txt && git add f.txt && git commit -qm init\n"
        f"sed -i '1,{a}d' f.txt\n"
        f"seq 21 {20 + b} >> f.txt\n")
    tid = f"gitdiff-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 3, "env",
        f"The repo has uncommitted changes to f.txt. How many lines were "
        f"added (git diff numstat)? Answer with just the number.",
        answer_mode="answer", max_turns=8, tags=["git"], template="git_diff_stat",
        seed=rng.randint(0, 10**6), split=split, setup_sh=setup_sh,
        test_py=answer_test(float(b), 0.0),
        solution_sh="git diff --numstat | head\ngit diff --numstat f.txt | cut -f1 > answer.txt\n")


# env_var test depends on the .key value; emit custom test
def _env_test():
    return '''\
import os
from pathlib import Path
BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_file_present():
    assert (BASE / "out.txt").exists()

def test_out():
    key = (BASE / ".key").read_text().strip()
    assert (BASE / "out.txt").read_text() == "ok-" + key + "\\n"
'''


def env_var(rng, idx, out_root, split):  # noqa: F811 (replaces stub above)
    prog = ("import os, sys\nv = os.environ.get('RUN_KEY')\n"
            "if v is None:\n    sys.exit('RUN_KEY not set')\nprint('ok-' + v)\n")
    tid = f"envvar-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "env",
        "app.py needs env var RUN_KEY. There is a file .key with the "
        "required value. Export it and run app.py writing output to "
        "out.txt.",
        answer_mode="files", max_turns=6, tags=["env"], template="env_var",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"app.py": prog, ".key": f"k{rng.randint(100,999)}\n"},
        test_py=_env_test(),
        solution_sh="cat .key\nRUN_KEY=$(cat .key) python3 app.py > out.txt\n")


# ---------------- train-only --------------------------------------------

def t_touch_flag(rng, idx, out_root, split):
    tid = f"ttouch-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "env",
        "Create an empty file named done.flag.",
        answer_mode="files", max_turns=3, tags=["touch"], template="t_touch_flag",
        seed=rng.randint(0, 10**6), split=split,
        test_py=files_test("done.flag", ""),
        solution_sh="touch done.flag\n")


def t_mkpath(rng, idx, out_root, split):
    p = rng.choice(["a/b/c", "x/y", "logs/2024"])
    tid = f"tmkp-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "env",
        f"Create nested directory '{p}' and an empty file '{p}/f.txt'.",
        answer_mode="files", max_turns=4, tags=["mkdir"], template="t_mkpath",
        seed=rng.randint(0, 10**6), split=split,
        test_py=files_test(f"{p}/f.txt", ""),
        solution_sh=f"mkdir -p {p}\ntouch {p}/f.txt\n")


def t_git_commit(rng, idx, out_root, split):
    setup_sh = ("git init -q . && git config user.email t@t && git config user.name t\n"
                "echo v1 > f.txt && git add f.txt && git commit -qm init\n")
    tid = f"tgitcom-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 2, "env",
        "Append 'v2' to f.txt and commit the change with message 'upd'.",
        answer_mode="files", max_turns=6, tags=["git"], template="t_git_commit",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"f.txt": "v1\n"}, setup_sh=setup_sh,
        test_py=('''\
import os, subprocess
from pathlib import Path
BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_file_present():
    assert (BASE / "f.txt").exists()

def test_committed():
    assert (BASE / "f.txt").read_text() == "v1\\nv2\\n"
    log = subprocess.run(["git", "-C", str(BASE), "log", "--format=%s"],
                         capture_output=True, text=True).stdout
    assert "upd" in log
'''),
        solution_sh="echo v2 >> f.txt\ngit add f.txt\ngit commit -qm upd\n")


def t_cleanup(rng, idx, out_root, split):
    files = {f"tmp{i}.tmp": "x\n" for i in range(rng.randint(3, 8))}
    files["keep.txt"] = "k\n"
    tid = f"tclean-{split}-{idx:03d}"
    return write_task(
        out_root, tid, 1, "env",
        "Delete all *.tmp files but keep keep.txt.",
        answer_mode="files", max_turns=4, tags=["rm"], template="t_cleanup",
        seed=rng.randint(0, 10**6), split=split, setup_files=files,
        test_py=('''\
import os
from pathlib import Path
BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_file_present():
    assert (BASE / "keep.txt").exists()

def test_cleaned():
    assert not list(BASE.glob("*.tmp")), "tmp files remain"
'''),
        solution_sh="rm -f *.tmp\nls\n")


def t_perm_read(rng, idx, out_root, split):
    tid = f"tperm-{split}-{idx:03d}"
    setup_sh = "chmod 000 secret.txt\n"
    return write_task(
        out_root, tid, 2, "env",
        "secret.txt is not readable (mode 000). Make it readable and copy "
        "its content to out.txt.",
        answer_mode="files", max_turns=5, tags=["chmod"], template="t_perm_read",
        seed=rng.randint(0, 10**6), split=split,
        setup_files={"secret.txt": f"s{rng.randint(10,99)}\n"}, setup_sh=setup_sh,
        test_py=('''\
import os
from pathlib import Path
BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_file_present():
    assert (BASE / "out.txt").exists()

def test_content():
    assert (BASE / "out.txt").read_text() == (BASE / "secret.txt").read_text()
'''),
        solution_sh="chmod +r secret.txt\ncat secret.txt > out.txt\n")
