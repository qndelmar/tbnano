"""Backend protocol."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Protocol

from ..tokens import Tokenizer


@dataclass
class BackendReply:
    text: str = ""
    # Structured tool calls (native-tools API models); None for text-only.
    native_tool_calls: Optional[list[dict[str, Any]]] = None
    usage_tokens: int = 0


class Backend(Protocol):
    name: str

    def generate(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
        max_tokens: int = 256,
        temperature: float = 0.0,
        seed: Optional[int] = None,
    ) -> BackendReply: ...

    def tokenizer(self) -> Tokenizer: ...

    def count_context(self, messages: list[dict[str, Any]]) -> int:
        """Tokens the running transcript occupies in the model's context.
        Default: per-message content + small per-message overhead."""
        tok = self.tokenizer()
        return sum(tok.count(str(m.get("content") or "")) + 8 for m in messages)
