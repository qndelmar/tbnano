"""The episode loop (spec sections 2-3).

One episode = one task attempt. Enforces every budget; the episode ends
with one of: finish | max_turns | context_overflow | timeout | no_call.
Old turns are never elided — fitting the context is part of the task.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Optional

from .adapters import Adapter
from .adapters.base import ParseStatus
from .backends.base import Backend
from .budgets import (
    MAX_CONTEXT_TOKENS,
    MAX_EXEC_SECONDS,
    MAX_RESPONSE_TOKENS,
    RUN_TIMEOUT_SECONDS,
)
from .sandbox.base import Sandbox
from .tasksio import TaskSpec
from .tokens import Tokenizer
from .tools import TOOL_SCHEMAS, ToolCall
from .truncate import truncate_tool_output

END_FINISH = "finish"
END_MAX_TURNS = "max_turns"
END_CONTEXT_OVERFLOW = "context_overflow"
END_TIMEOUT = "timeout"
END_NO_CALL = "no_call"

_NO_CALL_NUDGE = (
    "No tool call was detected in your reply. Respond with exactly one "
    "tool call in the required format, or finish() when done."
)
_ERROR_NUDGE = "Tool call error: {err}. Emit exactly one valid tool call."


@dataclass
class EpisodeResult:
    task_id: str
    end_reason: str
    answer: str = ""
    turns_used: int = 0
    tokens_used: int = 0          # peak context estimate, model tokens
    invalid_calls: int = 0
    exec_seconds: float = 0.0
    trajectory: list[dict[str, Any]] = field(default_factory=list)

    def summary_line(self) -> dict:
        d = asdict(self)
        d.pop("trajectory")
        return d


def _truncate_reply(text: str, tok: Tokenizer) -> str:
    if tok.count(text) <= MAX_RESPONSE_TOKENS:
        return text
    # Hard cap: ~4 chars/token, slightly generous, then recount-clamp.
    cut = text[: MAX_RESPONSE_TOKENS * 4]
    while tok.count(cut) > MAX_RESPONSE_TOKENS and cut:
        cut = cut[: int(len(cut) * 0.9)]
    return cut


def run_episode(
    spec: TaskSpec,
    backend: Backend,
    adapter: Adapter,
    sandbox: Sandbox,
    tok: Tokenizer,
    temperature: float = 0.0,
    seed: Optional[int] = None,
) -> EpisodeResult:
    res = EpisodeResult(task_id=spec.id, end_reason=END_MAX_TURNS)
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": adapter.system_prompt()},
        {"role": "user", "content": spec.instruction},
    ]
    res.tokens_used = backend.count_context(messages)
    if res.tokens_used > MAX_CONTEXT_TOKENS:
        res.end_reason = END_CONTEXT_OVERFLOW
        return res

    text_streak = 0
    tools_arg = adapter.schemas() if adapter.native_tools else None

    for turn in range(spec.max_turns):
        reply = backend.generate(
            adapter.to_chat(messages),
            tools=tools_arg,
            max_tokens=MAX_RESPONSE_TOKENS,
            temperature=temperature,
            seed=seed,
        )
        reply_text = _truncate_reply(reply.text or "", tok)

        if adapter.native_tools and reply.native_tool_calls:
            from .adapters.openai import OpenAIAdapter

            call = OpenAIAdapter.parse_native_call(reply.native_tool_calls)
            parsed_status = ParseStatus.CALL if call else ParseStatus.INVALID
            if call is None:
                err = "unparseable native tool call"
        else:
            pr = adapter.parse(reply_text)
            parsed_status = pr.status
            call = pr.call
            err = pr.error

        if parsed_status == ParseStatus.TEXT:
            text_streak += 1
            messages.append({"role": "assistant", "content": reply_text})
            res.trajectory.append(
                {"turn": turn, "reply": reply_text, "kind": "text"}
            )
            if text_streak >= 2:
                res.end_reason = END_NO_CALL
                res.turns_used = turn + 1
                _update_tokens(res, backend, messages)
                return res
            messages.append({"role": "user", "content": _NO_CALL_NUDGE})
            continue
        text_streak = 0

        if parsed_status == ParseStatus.INVALID or call is None:
            res.invalid_calls += 1
            messages.append({"role": "assistant", "content": reply_text})
            messages.append(
                {"role": "tool", "content": _ERROR_NUDGE.format(err=err)}
            )
            res.trajectory.append(
                {"turn": turn, "reply": reply_text, "kind": "invalid", "error": err}
            )
            continue

        messages.append({"role": "assistant", "content": reply_text})
        res.trajectory.append(
            {"turn": turn, "reply": reply_text, "kind": "call", "call": call.to_json()}
        )

        if call.name == "finish":
            res.answer = str(call.arguments.get("answer", "") or "")
            res.end_reason = END_FINISH
            res.turns_used = turn + 1
            _update_tokens(res, backend, messages)
            return res

        result_json, elapsed, _timed_out = _exec_call(call, sandbox)
        res.exec_seconds += elapsed
        if res.exec_seconds > MAX_EXEC_SECONDS:
            res.end_reason = END_TIMEOUT
            res.turns_used = turn + 1
            _update_tokens(res, backend, messages)
            return res

        out = truncate_tool_output(adapter.tool_result_content(result_json), tok)
        messages.append({"role": "tool", "content": out})
        res.trajectory[-1]["result"] = out

        ctx = backend.count_context(messages)
        res.tokens_used = max(res.tokens_used, ctx)
        if ctx > MAX_CONTEXT_TOKENS:
            res.end_reason = END_CONTEXT_OVERFLOW
            res.turns_used = turn + 1
            return res

    res.turns_used = spec.max_turns
    res.end_reason = END_MAX_TURNS
    _update_tokens(res, backend, messages)
    return res


def _update_tokens(res: EpisodeResult, backend: Backend, messages) -> None:
    res.tokens_used = max(res.tokens_used, backend.count_context(messages))


def _exec_call(call: ToolCall, sandbox: Sandbox) -> tuple[str, float, bool]:
    """Dispatch a tool call to the sandbox. Returns (json, elapsed, timed_out)."""
    a = call.arguments or {}
    if call.name == "run":
        cmd = str(a.get("cmd", ""))
        if not cmd.strip():
            return json.dumps({"error": "empty cmd"}), 0.0, False
        r = sandbox.run(cmd, timeout=RUN_TIMEOUT_SECONDS)
        return r.to_tool_json(), r.elapsed, r.timed_out
    if call.name == "read_file":
        out = sandbox.read_file(
            str(a.get("path", "")),
            start=int(a.get("start", 1) or 1),
            lines=int(a.get("lines", 60) or 60),
        )
        return json.dumps(out), 0.0, False
    if call.name == "write_file":
        out = sandbox.write_file(str(a.get("path", "")), str(a.get("content", "")))
        return json.dumps(out), 0.0, False
    return json.dumps({"error": f"unknown tool {call.name}"}), 0.0, False


# Schemas for episode<->harness plumbing
def tool_schemas() -> list[dict]:
    return TOOL_SCHEMAS
