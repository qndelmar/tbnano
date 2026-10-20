"""Honest head/tail truncation of tool output."""

from tbnano.budgets import MAX_TOOL_OUTPUT_TOKENS
from tbnano.tokens import ApproxTokenizer
from tbnano.truncate import truncate_tool_output

TOK = ApproxTokenizer()


def test_short_unchanged():
    s = "hello\nworld\n"
    assert truncate_tool_output(s, TOK) == s


def test_long_has_marker_head_tail():
    lines = [f"line {i} " + "x" * 40 for i in range(200)]
    s = "\n".join(lines)
    out = truncate_tool_output(s, TOK)
    assert TOK.count(out) <= MAX_TOOL_OUTPUT_TOKENS + 8
    assert "lines cut" in out
    assert out.startswith("line 0")
    assert "line 199" in out  # tail kept


def test_cut_count_is_honest():
    lines = [f"row{i}\n" for i in range(500)]
    s = "".join(lines)
    out = truncate_tool_output(s, TOK)
    import re

    m = re.search(r"\.\.\. \[(\d+) lines cut\] \.\.\.", out)
    assert m, out[:200]
    cut = int(m.group(1))
    assert cut > 0


def test_budget_enforced():
    s = "y" * 100000
    out = truncate_tool_output(s, TOK)
    assert TOK.count(out) <= MAX_TOOL_OUTPUT_TOKENS + 8
