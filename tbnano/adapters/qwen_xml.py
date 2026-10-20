"""Qwen3.5 / Qwen3-Coder XML format, what Qwen3.5's own chat template asks for:

    <tool_call>
    <function=run>
    <parameter=cmd>
    ls -la
    </parameter>
    </function>
    </tool_call>

Parameter values are raw text (no JSON quoting); integers are converted for
integer-typed schema params. A leading <think>...</think> block is ignored.
"""

from __future__ import annotations

import re

from ..tools import TOOL_NAMES, TOOL_SCHEMAS, ToolCall
from .base import Adapter, ParseResult, ParseStatus

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)
_CALL_RE = re.compile(r"<tool_call>(.*?)</tool_call>", re.DOTALL)
_FUNC_RE = re.compile(r"<function=([\w.-]+)>(.*?)</function>", re.DOTALL)
_PARAM_RE = re.compile(r"<parameter=([\w.-]+)>\n?(.*?)\n?</parameter>", re.DOTALL)
_OPEN_TAG = "<tool_call>"

_INT_PARAMS = {
    t["function"]["name"]: {k for k, v in t["function"]["parameters"].get("properties", {}).items()
                            if v.get("type") == "integer"}
    for t in TOOL_SCHEMAS
}


class QwenXmlAdapter(Adapter):
    name = "qwen_xml"

    def call_syntax_help(self) -> str:
        return (
            "To call a tool, reply with exactly:\n"
            "<tool_call>\n<function=TOOL>\n<parameter=ARG>\nVALUE\n</parameter>\n</function>\n</tool_call>\n"
            "Example: <tool_call>\n<function=run>\n<parameter=cmd>\nls -la\n</parameter>\n</function>\n</tool_call>"
        )

    def parse(self, reply: str) -> ParseResult:
        text = _THINK_RE.sub("", reply)
        m = _CALL_RE.search(text)
        if m is None:
            if _OPEN_TAG in text:
                return ParseResult(ParseStatus.INVALID, error="unterminated <tool_call> tag", text=reply)
            return ParseResult(ParseStatus.TEXT, text=reply)
        f = _FUNC_RE.search(m.group(1))
        if f is None:
            return ParseResult(ParseStatus.INVALID, error="no <function=...> block in tool call", text=reply)
        name = f.group(1)
        if name not in TOOL_NAMES:
            return ParseResult(ParseStatus.INVALID, error=f"unknown tool {name!r}", text=reply)
        args: dict = {}
        for k, v in _PARAM_RE.findall(f.group(2)):
            if k in _INT_PARAMS.get(name, ()):
                try:
                    args[k] = int(v.strip())
                    continue
                except ValueError:
                    return ParseResult(ParseStatus.INVALID, error=f"{k} must be an integer", text=reply)
            args[k] = v
        return ParseResult(ParseStatus.CALL, call=ToolCall(name=name, arguments=args, raw=m.group(0)))
