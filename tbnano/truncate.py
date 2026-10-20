"""Honest output truncation (spec section 2).

A single tool output is capped at MAX_TOOL_OUTPUT_TOKENS tokens. Truncation
keeps the head and the tail of the output and replaces the middle with a
visible marker: ``... [N lines cut] ...`` so the model sees that content
was elided (no silent data loss).
"""

from __future__ import annotations

from .budgets import MAX_TOOL_OUTPUT_TOKENS
from .tokens import Tokenizer


def truncate_text(text: str, max_tokens: int, tok: Tokenizer) -> str:
    """Truncate ``text`` to ``max_tokens`` keeping head and tail lines."""
    if tok.count(text) <= max_tokens:
        return text

    lines = text.splitlines(keepends=True)
    if not lines:
        return text[: max_tokens * 4]

    marker_tpl = "... [{} lines cut] ...\n"
    # Reserve ~1/3 of the budget for the tail, 2/3 for the head.
    head: list[str] = []
    head_tokens = 0
    head_budget = int(max_tokens * 0.66)
    for line in lines:
        n = tok.count(line)
        if head_tokens + n > head_budget:
            break
        head.append(line)
        head_tokens += n

    tail: list[str] = []
    tail_tokens = 0
    tail_budget = max_tokens - head_budget - tok.count(marker_tpl.format(9999))
    for line in reversed(lines[len(head):]):
        n = tok.count(line)
        if tail_tokens + n > tail_budget:
            break
        tail.append(line)
        tail_tokens += n
    tail.reverse()

    kept = len(head) + len(tail)
    cut = len(lines) - kept
    if cut <= 0:
        # Could not represent the cut honestly; hard-truncate the head.
        return "".join(head) or text[: max_tokens * 4]

    return "".join(head) + marker_tpl.format(cut) + "".join(tail)


def truncate_tool_output(text: str, tok: Tokenizer) -> str:
    return truncate_text(text, MAX_TOOL_OUTPUT_TOKENS, tok)
