"""OpenAI-compatible API backend (spec: api:<model>, upper-bound calibration).

Uses native tool calling via the chat.completions `tools` parameter. Token
counting is approximate (tiktoken) since the real tokenizer is remote —
as the spec allows.
"""

from __future__ import annotations

import os
from typing import Any, Optional

from ..tokens import TiktokenTokenizer, Tokenizer
from .base import BackendReply


class APIBackend:
    name = "api"

    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self.model = model
        self.base_url = base_url or os.environ.get("TBNANO_API_BASE")
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY") or "EMPTY"
        self._client = None
        self._tok = TiktokenTokenizer(model)

    def _client_lazy(self):
        if self._client is None:
            from openai import OpenAI

            self._client = OpenAI(
                base_url=self.base_url or None, api_key=self.api_key
            )
        return self._client

    def tokenizer(self) -> Tokenizer:
        return self._tok

    def generate(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
        max_tokens: int = 256,
        temperature: float = 0.0,
        seed: Optional[int] = None,
    ) -> BackendReply:
        client = self._client_lazy()
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": _api_messages(messages),
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if tools:
            kwargs["tools"] = tools
        if seed is not None:
            kwargs["seed"] = seed
        resp = client.chat.completions.create(**kwargs)
        msg = resp.choices[0].message
        tcs = None
        if msg.tool_calls:
            tcs = [
                {
                    "id": tc.id,
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in msg.tool_calls
            ]
        return BackendReply(
            text=msg.content or "",
            native_tool_calls=tcs,
            usage_tokens=getattr(resp.usage, "total_tokens", 0) or 0,
        )


def _api_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Canonical transcript -> chat.completions messages.

    Our canonical tool results carry plain JSON text; the API wants
    role=tool with a tool_call_id, which we synthesise.
    """
    out = []
    n = 0
    for m in messages:
        if m.get("role") == "tool":
            n += 1
            out.append(
                {
                    "role": "tool",
                    "tool_call_id": f"call_{n}",
                    "content": m["content"],
                }
            )
        elif m.get("role") == "assistant" and "tool_call" in m:
            out.append({"role": "assistant", "content": m.get("content")})
        else:
            out.append({"role": m["role"], "content": m.get("content") or ""})
    return out
