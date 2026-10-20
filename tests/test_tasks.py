"""Task-format and generator sanity checks."""

import random
from pathlib import Path

import pytest

from tbnano.budgets import MAX_INSTRUCTION_TOKENS
from tbnano.generators import TEST_TEMPLATES, TRAIN_TEMPLATES
from tbnano.runner import split_script
from tbnano.tasksio import load_task, task_fingerprints, validate_task
from tbnano.tokens import ApproxTokenizer

TOK = ApproxTokenizer()


def test_split_script_heredoc():
    script = "#!/bin/bash\nset -e\n# comment\n\ncat > f.py <<'EOF'\nline1\nline2\nEOF\necho done\n"
    cmds = split_script(script)
    assert len(cmds) == 2
    assert "line1" in cmds[0] and cmds[1] == "echo done"


def test_split_script_multiline_quote():
    script = 'python3 -c "\nimport csv\nprint(1)\n" > answer.txt\necho hi\n'
    cmds = split_script(script)
    assert len(cmds) == 2
    assert cmds[0].startswith('python3 -c "')


def test_template_sets_disjoint():
    shared = set(TEST_TEMPLATES) & set(TRAIN_TEMPLATES)
    assert not shared, f"templates shared across splits: {shared}"


def test_n_templates():
    assert len(TEST_TEMPLATES) >= 60
    assert len(TRAIN_TEMPLATES) >= 30


@pytest.mark.parametrize("name", sorted(TEST_TEMPLATES))
def test_template_generates_valid_task(tmp_path, name):
    res = TEST_TEMPLATES[name](random.Random(7), 0, tmp_path, "test")
    # L0 generators return a guided+plain pair
    dirs = res if isinstance(res, list) else [res]
    for d in dirs:
        spec = load_task(d)
        problems = validate_task(spec, TOK)
        assert problems == [], f"{name}: {problems}"
        assert spec.template == name
        assert TOK.count(spec.instruction) <= MAX_INSTRUCTION_TOKENS
        assert (d / "solution.sh").exists()
    if name.startswith("l0_"):
        assert len(dirs) == 2
        tracks = {load_task(d).track for d in dirs}
        assert tracks == {"guided", "plain"}
        # same files and checks for both variants (spec v2 2)
        assert {f.name for f in (dirs[0] / "setup").rglob("*")} == \
               {f.name for f in (dirs[1] / "setup").rglob("*")}
        assert (dirs[0] / "tests" / "test.py").read_text() == \
               (dirs[1] / "tests" / "test.py").read_text()


@pytest.mark.parametrize("name", sorted(TRAIN_TEMPLATES))
def test_train_template_generates_valid_task(tmp_path, name):
    res = TRAIN_TEMPLATES[name](random.Random(7), 0, tmp_path, "train")
    for d in (res if isinstance(res, list) else [res]):
        spec = load_task(d)
        problems = validate_task(spec, TOK)
        assert problems == [], f"{name}: {problems}"
        assert spec.template == name


def test_fingerprints_differ_across_seeds(tmp_path):
    gen = TEST_TEMPLATES["log_count"]
    a = gen(random.Random(1), 0, tmp_path / "a", "test")
    b = gen(random.Random(2), 1, tmp_path / "b", "test")
    fa = task_fingerprints(load_task(a))
    fb = task_fingerprints(load_task(b))
    assert not (fa & fb)


def test_system_prompt_fits_budget():
    from tbnano.budgets import MAX_SYSTEM_TOKENS
    from tbnano.adapters import get_adapter

    for fmt in ("json_tags", "lfm_pythonic", "hermes", "openai"):
        a = get_adapter(fmt)
        assert TOK.count(a.system_prompt()) <= MAX_SYSTEM_TOKENS
