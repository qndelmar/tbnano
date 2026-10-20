"""LiquidAI LFM2.x pythonic format: <|tool_call_start|>[run(cmd="ls")]<|tool_call_end|>.

The payload is a Python list of function-call expressions. Parsed with the
`ast` module only — never eval.
"""

from __future__ import annotations

import ast
import re
from typing import Any

from ..tools import TOOL_NAMES, TOOL_SCHEMAS, ToolCall
from .base import Adapter, ParseResult, ParseStatus

_CALL_RE = re.compile(
    r"<\|tool_call_start\|>(.*?)<\|tool_call_end\|>", re.DOTALL
)
_OPEN_TAG = "<|tool_call_start|>"

# name -> ordered positional parameter names, from the JSON schemas.
_POS_PARAMS: dict[str, list[str]] = {
    t["function"]["name"]: [
        p for p in t["function"]["parameters"].get("properties", {})
    ]
    for t in TOOL_SCHEMAS
}


def _literal(node: ast.AST) -> Any:
    """Evaluate a node restricted to literals (ast.literal_eval)."""
    return ast.literal_eval(node)


def _call_node_to_toolcall(node: ast.AST, raw: str) -> ToolCall:
    if not isinstance(node, ast.Call):
        raise ValueError("list items must be function calls")
    if isinstance(node.func, ast.Name):
        name = node.func.id
    else:
        raise ValueError("callee must be a bare function name")
    if name not in TOOL_NAMES:
        raise ValueError(f"unknown tool {name!r}")

    args: dict[str, Any] = {}
    pos = _POS_PARAMS[name]
    for i, a in enumerate(node.args):
        if i >= len(pos):
            raise ValueError(f"too many positional args for {name}")
        args[pos[i]] = _literal(a)
    for kw in node.keywords:
        if kw.arg is None:
            raise ValueError("**kwargs not allowed")
        args[kw.arg] = _literal(kw.value)
    return ToolCall(name=name, arguments=args, raw=raw)


class LfmPythonicAdapter(Adapter):
    name = "lfm_pythonic"

    def call_syntax_help(self) -> str:
        return (
            "To call a tool, reply with exactly:\n"
            "<|tool_call_start|>[<tool>(<arg>=<value>)]<|tool_call_end|>\n"
            'Example: <|tool_call_start|>[run(cmd="ls -la")]<|tool_call_end|>'
        )

    def parse(self, reply: str) -> ParseResult:
        m = _CALL_RE.search(reply)
        if m is None:
            if _OPEN_TAG in reply:
                return ParseResult(
                    ParseStatus.INVALID,
                    error="unterminated <|tool_call_start|> tag",
                    text=reply,
                )
            return ParseResult(ParseStatus.TEXT, text=reply)

        payload = m.group(1).strip()
        try:
            tree = ast.parse(payload, mode="eval")
            calls = tree.body
            if not isinstance(calls, ast.List):
                calls = ast.List(elts=[calls])
            if not calls.elts:
                raise ValueError("empty call list")
            call = _call_node_to_toolcall(calls.elts[0], m.group(0))
        except (SyntaxError, ValueError, TypeError) as e:
            return ParseResult(
                ParseStatus.INVALID,
                error=f"cannot parse pythonic call: {e}",
                text=reply,
            )
        return ParseResult(ParseStatus.CALL, call=call)
