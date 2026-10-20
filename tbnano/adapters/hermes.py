"""Hermes / Qwen format: <tool_call>{json}</tool_call>."""

from __future__ import annotations

import json
import re

from ..tools import TOOL_NAMES, ToolCall
from .base import Adapter, ParseResult, ParseStatus

_CALL_RE = re.compile(r"<tool_call>(.*?)</tool_call>", re.DOTALL)
_OPEN_TAG = "<tool_call>"


class HermesAdapter(Adapter):
    name = "hermes"

    def call_syntax_help(self) -> str:
        return (
            "To call a tool, reply with exactly:\n"
            '<tool_call>{"name": "<tool>", "arguments": {<args>}}</tool_call>\n'
            'Example: <tool_call>{"name": "run", "arguments": {"cmd": "ls -la"}}'
            "</tool_call>"
        )

    def parse(self, reply: str) -> ParseResult:
        m = _CALL_RE.search(reply)
        if m is None:
            if _OPEN_TAG in reply:
                return ParseResult(
                    ParseStatus.INVALID,
                    error="unterminated <tool_call> tag",
                    text=reply,
                )
            return ParseResult(ParseStatus.TEXT, text=reply)

        payload = m.group(1).strip()
        try:
            obj = json.loads(payload)
        except json.JSONDecodeError as e:
            return ParseResult(
                ParseStatus.INVALID, error=f"bad JSON in tool call: {e}", text=reply
            )
        if not isinstance(obj, dict) or "name" not in obj:
            return ParseResult(
                ParseStatus.INVALID,
                error='tool call must be {"name": ..., "arguments": {...}}',
                text=reply,
            )
        name = obj["name"]
        args = obj.get("arguments", {})
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except json.JSONDecodeError:
                pass
        if not isinstance(args, dict):
            return ParseResult(
                ParseStatus.INVALID, error="arguments must be an object", text=reply
            )
        if name not in TOOL_NAMES:
            return ParseResult(
                ParseStatus.INVALID, error=f"unknown tool {name!r}", text=reply
            )
        return ParseResult(
            ParseStatus.CALL, call=ToolCall(name=name, arguments=args, raw=m.group(0))
        )
