"""OpenAI-format adapter: native tool_calls (for API calibration models).

The model sees the real JSON schemas via the API's `tools` parameter, so
parse() is only a fallback for models that emit Hermes-style text anyway.
"""

from __future__ import annotations

from ..tools import TOOL_SCHEMAS, ToolCall
from .base import Adapter, ParseResult, ParseStatus
from .hermes import HermesAdapter

_fallback = HermesAdapter()


class OpenAIAdapter(Adapter):
    name = "openai"
    native_tools = True

    def system_prompt(self, schemas_in_template: bool = False, text_final: bool = False) -> str:
        # Tool schemas go through the API `tools` param; the system prompt
        # only needs the rules.
        return (
            "You operate in a Linux terminal via tool calls. Exactly one tool "
            "call per reply. `run` executes `bash -lc` in /task with empty "
            "stdin and a 10s timeout; no interactive programs, no network. "
            "Long tool output is truncated with '... [N lines cut] ...'. "
            "Call finish() when done; pass `answer` when the task asks for one."
        )

    def schemas(self) -> list[dict]:
        return TOOL_SCHEMAS

    def parse(self, reply: str) -> ParseResult:
        # For API backends the reply comes pre-parsed via parse_native_call;
        # this is only a fallback when the model returned markup as text.
        return _fallback.parse(reply)

    @staticmethod
    def parse_native_call(tool_calls: list[dict]) -> ToolCall | None:
        """Convert an API tool_calls list into a canonical ToolCall."""
        if not tool_calls:
            return None
        tc = tool_calls[0]
        fn = tc.get("function", {})
        import json

        try:
            args = json.loads(fn.get("arguments", "{}") or "{}")
        except json.JSONDecodeError:
            args = {}
        return ToolCall(name=fn.get("name", ""), arguments=args, raw=str(tc))
