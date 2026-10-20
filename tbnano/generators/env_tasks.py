"""Environment family (spec 5.3, ~10%): perms, paths, git."""

from __future__ import annotations

import random
from pathlib import Path

from .base import pick, with_id, write_task


def gen_paths_perms(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    tid = f"paths-{split}-{idx:03d}"
    variant = rng.choice(["chmod", "misplaced_conf", "missing_dir"])
    out_name = pick(rng, ["out.txt", "result.txt", "done.txt"],
                    ["flag.txt", "res.txt", "end.txt"], split)
    payload = f"payload-{rng.randint(1000,9999)}"

    if variant == "chmod":
        script = pick(rng, ["run.sh", "go.sh"], ["exec.sh", "launch.sh"], split)
        setup = {
            script: with_id(f"#!/bin/bash\necho {payload} > {out_name}\n", tid),
        }
        instr = (
            f"./{script} exists but `./{script}` fails with 'permission denied'. "
            f"Make it work and run it so that {out_name} is created."
        )
        sol = f"chmod +x {script} && ./{script}\n"
    elif variant == "misplaced_conf":
        conf = pick(rng, ["app.conf", "svc.conf"], ["node.conf", "agent.conf"], split)
        good_dir = pick(rng, ["conf"], ["etc"], split)
        setup = {
            conf: f"secret={payload}\n",
            "loader.sh": with_id(
                "#!/bin/bash\n"
                "set -e\n"
                f"cat {good_dir}/{conf} > /dev/null || {{ echo '{good_dir}/{conf} not found' >&2; exit 1; }}\n"
                f"cp {good_dir}/{conf} {out_name}\n",
                tid,
            ),
        }
        instr = (
            f"./loader.sh expects its config at {good_dir}/{conf}, but {conf} "
            f"sits in the wrong place. Fix the layout and run loader.sh so "
            f"{out_name} is produced."
        )
        sol = f"mkdir -p {good_dir} && mv {conf} {good_dir}/ && bash loader.sh\n"
    else:
        script = pick(rng, ["deploy.sh", "ship.sh"], ["push.sh", "stage.sh"], split)
        target_dir = pick(rng, ["deployed", "out_dir"], ["staging", "drop"], split)
        flag = pick(rng, ["flag.txt", "marker.txt"], ["ok.txt", "done.txt"], split)
        setup = {
            script: with_id(
                "#!/bin/bash\nset -e\n"
                f"echo {payload} > {target_dir}/{flag}\n",
                tid,
            ),
        }
        instr = (
            f"./{script} fails because the target directory does not exist "
            f"and the script cannot create it. Make the run succeed so that "
            f"{target_dir}/{flag} exists."
        )
        sol = f"mkdir -p {target_dir} && bash {script}\n"
        expected_path = f"{target_dir}/{flag}"

    if variant != "missing_dir":
        expected_path = out_name
    return write_task(
        out_root, tid, level=2, category="env",
        instruction=instr, answer_mode="files", max_turns=6,
        tags=["perms", "paths"], seed=rng.randint(0, 10**6), split=split,
        setup_files=setup,
        test_py=f'''\
import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "{expected_path}"
    assert p.exists(), "{expected_path} missing"
    assert "{payload}" in p.read_text()
''',
        solution_sh=sol,
    )


WORDS = ["hyperdrive", "antenna", "gyro", "telemetry", "payload", "booster"]


def gen_git_restore(rng: random.Random, idx: int, out_root: Path, split: str) -> Path:
    fname = pick(rng, ["notes.txt", "config.ini", "manifest.txt", "crew.txt"],
                 ["diary.txt", "prefs.ini", "index.txt", "team.txt"], split)
    word = rng.choice(WORDS)
    secret = f"{word}-{rng.randint(100, 999)}"
    n_noise = rng.randint(0, 2)
    noise_cmds = "\n".join(
        f"echo noise{i} > other{i}.txt && git add -A && "
        "git -c user.email=a@b -c user.name=x commit -qm noise" + str(i)
        for i in range(n_noise)
    )
    # history: commit1 creates fname, noise commits, then deletion at HEAD.
    setup_sh = f"""\
git init -q .
git config user.email t@t && git config user.name t
echo "{secret}" > {fname}
git add -A && git -c user.email=a@b -c user.name=x commit -qm "add {fname}"
{noise_cmds}
git rm -q {fname} && git -c user.email=a@b -c user.name=x commit -qm "remove {fname}"
"""
    instr = (
        f"{fname} was deleted in the latest commit. Restore its previous "
        f"version from git history into the working tree."
    )
    sol = f"git checkout HEAD~1 -- {fname}\n"
    tid = f"gitrest-{split}-{idx:03d}"
    return write_task(
        out_root, tid, level=3, category="env",
        instruction=instr, answer_mode="files", max_turns=8,
        tags=["git", "restore"], seed=rng.randint(0, 10**6), split=split,
        setup_sh=setup_sh,
        test_py=f'''\
import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_restored():
    p = BASE / "{fname}"
    assert p.exists(), "{fname} not restored"
    assert "{secret}" in p.read_text()
''',
        solution_sh=sol,
    )
