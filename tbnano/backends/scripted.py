"""Scripted backend — deterministic fake model for tbnano's own validation.

Script forms (the part after `scripted:`):
    quitter            -> immediately emits a finish() call
    echo:<fmt>         -> always emits `run(cmd="echo hi")` once, then finish
    oracle             -> replays the task's solution.sh line-by-line through
                          run(), then finishes with the contents of
                          /task/answer.txt if present
    file:<path>        -> newline-separated replies consumed in order

The oracle is driven from outside via `set_oracle(lines)` before each
episode — see agents/oracle behaviour in runner.py.
"""

from __future__ import annotations

import json
from typing import Any, Optional

from ..tokens import ApproxTokenizer, Tokenizer
from .base import BackendReply


class ScriptedBackend:
    name = "scripted"

    def __init__(self, script: str = "quitter", **_):
        self.script = script
        self._tok = ApproxTokenizer()
        self._oracle_lines: list[str] = []
        self._file_replies: list[str] = []
        if script.startswith("file:"):
            with open(script[5:]) as f:
                self._file_replies = [l.rstrip("\n") for l in f if l.strip()]

    def set_oracle(self, lines: list[str]) -> None:
        self._oracle_lines = list(lines)

    # -- reply selection -------------------------------------------------
    def _next(self, step: int) -> str:
        s = self.script
        if s == "quitter":
            return self._call("finish", {"answer": ""})
        if s == "oracle":
            if step < len(self._oracle_lines):
                return self._call("run", {"cmd": self._oracle_lines[step]})
            if step == len(self._oracle_lines):
                # Probe for a final answer file written by the solution.
                return self._call(
                    "run",
                    {"cmd": "cat answer.txt 2>/dev/null || cat /task/answer.txt 2>/dev/null || true"},
                )
            return self._call("finish", {"answer": self._oracle_answer})
        if s.startswith("echo"):
            if step == 0:
                return self._call("run", {"cmd": "echo hi"})
            return self._call("finish", {"answer": ""})
        if s.startswith("file:"):
            if step < len(self._file_replies):
                return self._file_replies[step]
            return self._call("finish", {"answer": ""})
        return self._call("finish", {"answer": ""})

    # `generate` is stateful: it tracks the step and, for the oracle, the
    # last tool output so it can extract the answer.
    def generate(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
        max_tokens: int = 256,
        temperature: float = 0.0,
        seed: Optional[int] = None,
    ) -> BackendReply:
        step = getattr(self, "_step", 0)
        # Record the last tool output for the oracle's finish answer.
        last_tool = next(
            (m for m in reversed(messages) if m.get("role") == "tool"), None
        )
        if self.script == "oracle" and last_tool is not None:
            try:
                out = json.loads(last_tool["content"])
                self._oracle_answer = (out.get("stdout") or "").strip().splitlines()
                self._oracle_answer = (
                    self._oracle_answer[-1] if self._oracle_answer else ""
                )
            except Exception:
                pass
        self._step = step + 1
        return BackendReply(text=self._next(step))

    def _call(self, name: str, args: dict) -> str:
        return (
            "<|tool_call|>"
            + json.dumps({"name": name, "arguments": args})
            + "<|tool_call_end|>"
        )

    def tokenizer(self) -> Tokenizer:
        return self._tok

    def count_context(self, messages) -> int:
        return sum(
            self._tok.count(str(m.get("content") or "")) + 8 for m in messages
        )

    def reset(self) -> None:
        self._step = 0
        self._oracle_answer = ""
