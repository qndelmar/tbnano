"""Task-format and generator sanity checks."""

import random
from pathlib import Path

import pytest

from tbnano.budgets import MAX_INSTRUCTION_TOKENS
from tbnano.generators import FAMILIES
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


@pytest.mark.parametrize("fam", sorted(FAMILIES))
def test_family_generates_valid_task(tmp_path, fam):
    d = FAMILIES[fam](random.Random(7), 0, tmp_path, "test")
    spec = load_task(d)
    problems = validate_task(spec, TOK)
    assert problems == [], f"{fam}: {problems}"
    assert TOK.count(spec.instruction) <= MAX_INSTRUCTION_TOKENS
    assert (d / "solution.sh").exists()


def test_fingerprints_differ_across_seeds(tmp_path):
    a = FAMILIES["log_count"](random.Random(1), 0, tmp_path / "a", "test")
    b = FAMILIES["log_count"](random.Random(2), 1, tmp_path / "b", "test")
    fa = task_fingerprints(load_task(a))
    fb = task_fingerprints(load_task(b))
    assert not (fa & fb)


def test_system_prompt_fits_budget():
    from tbnano.budgets import MAX_SYSTEM_TOKENS

    for fmt in ("json_tags", "lfm_pythonic", "hermes", "openai"):
        a = __import__("tbnano.adapters", fromlist=["get_adapter"]).get_adapter(fmt)
        assert TOK.count(a.system_prompt()) <= MAX_SYSTEM_TOKENS
