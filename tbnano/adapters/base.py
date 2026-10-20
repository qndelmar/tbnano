"""Adapter protocol and shared parsing helpers."""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Any, Optional

from ..tools import TOOLS_BRIEF, ToolCall


class ParseStatus(enum.Enum):
    CALL = "call"          # a valid tool call
    TEXT = "text"          # plain text, no call markup at all
    INVALID = "invalid"    # call markup present but unparseable / unknown tool


@dataclass
class ParseResult:
    status: ParseStatus
    call: Optional[ToolCall] = None
    error: str = ""
    text: str = ""          # the reply text (used for TEXT and for logging)


class Adapter:
    """One adapter per model-family call format.

    Adapters know three things: how to describe the tools to the model
    (system_prompt), how to turn a model reply into a ToolCall (parse),
    and how the running transcript maps onto chat-template messages
    (to_chat). Everything else stays canonical.
    """

    name: str = "base"
    # True for API models that emit structured tool_calls instead of text.
    native_tools: bool = False

    def system_prompt(self) -> str:
        """Tool schema block + rules. Must stay <= 600 tokens."""
        return TOOLS_BRIEF + "\n" + self.call_syntax_help()

    def call_syntax_help(self) -> str:
        """One short paragraph showing the exact call syntax to the model."""
        raise NotImplementedError

    def parse(self, reply: str) -> ParseResult:
        raise NotImplementedError

    def tool_result_content(self, result_json: str) -> str:
        """How a tool result is wrapped before being fed back to the model."""
        return result_json

    def to_chat(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Map canonical messages to chat-template dicts.

        Canonical roles: system / user / assistant / tool. Assistant
        messages may carry ``content`` (raw model reply). Tool results are
        canonical {"role": "tool", "content": result_json}. The default
        mapping is identity; adapters may re-wrap tool results.
        """
        return messages
