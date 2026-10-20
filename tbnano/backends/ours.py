"""Backend for our own checkpoints (`ckpt:<path>`).

Spec 3/7 + review: for our models the chat template is `render()` from
`chat_format.py` in our training repo, and inference is a wrapper over
`agent.py` exposing

    model, tok, device = agent.load(ckpt_path)
    out_ids = agent.generate(model, tok, ids, device, max_new=..., temp=...)

taking *token ids*; the tokenizer is `tokenizer/tokenizer.json`
(`tokenizers.Tokenizer`); `chat_format.render` expects
`assistant.tool_calls`, `{"role": "tool", "responses": [...]}` and a
`tools=` list, and we append `<|im_start|>assistant\n` ourselves
(reference: Agent._prompt_ids / Agent.reply in ../agent.py).

Point tbnano at that repo with TBNANO_OURS_REPO (default:
../small-test-llm). Our models are trained at ctx 1024 → max_context.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional

from .base import BackendReply

GEN_PROMPT_SUFFIX = "<|im_start|>assistant\n"


def _import_from(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_CALL_RE = re.compile(r"<\|tool_call\|>(.*?)(?:<\|tool_call_end\|>|$)", re.DOTALL)


def _flat_tools() -> list[dict]:
    """Our SFT data lists tools as flat {"name", "description", "parameters"} (prepare_midtrain.READ_ARTICLE)."""
    from ..tools import TOOL_SCHEMAS
    return [t["function"] for t in TOOL_SCHEMAS]


def _to_ours(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """tbnano canonical messages -> chat_format.render messages: raw call markup in assistant
    replies becomes tool_calls (render strips special tokens out of content), tool results
    become {"role": "tool", "responses": [...]}."""
    out = []
    for m in messages:
        if m.get("role") == "tool":
            c = m.get("content") or ""
            try:
                r = json.loads(c)
            except (json.JSONDecodeError, TypeError):
                r = c
            out.append({"role": "tool", "responses": [r]})
        elif m.get("role") == "assistant":
            text = m.get("content") or ""
            calls = []
            for payload in _CALL_RE.findall(text):
                try:
                    calls.append(json.loads(payload))
                except json.JSONDecodeError:
                    pass
            out.append({"role": "assistant", "content": _CALL_RE.sub("", text).strip(), "tool_calls": calls})
        else:
            out.append({"role": m["role"], "content": m.get("content") or ""})
    return out


class OursBackend:
    name = "ours"
    max_context = 1024  # our checkpoints train at ctx 1024
    renders_tools = True  # render(tools=...) lists the schemas in the system turn, as in our SFT data

    def __init__(self, ckpt: str, repo: Optional[str] = None, **_):
        self.ckpt = ckpt
        self.repo = Path(
            repo or os.environ.get("TBNANO_OURS_REPO", "../small-test-llm")
        ).resolve()
        self._model = None
        self._device = None
        self._agent_mod = None
        self._render = None
        self._tok = None

    def _load(self) -> None:
        if self._agent_mod is not None:
            return
        agent_py = self.repo / "agent.py"
        fmt_py = self.repo / "chat_format.py"
        tok_json = self.repo / "tokenizer" / "tokenizer.json"
        for p in (agent_py, fmt_py, tok_json):
            if not p.exists():
                raise FileNotFoundError(
                    f"ours backend needs {p} (set TBNANO_OURS_REPO)"
                )
        if str(self.repo) not in sys.path:  # chat_format/agent import sibling modules (data_mix, model_torch)
            sys.path.insert(0, str(self.repo))
        fmt = _import_from(fmt_py, "ours_chat_format")
        self._render = fmt.render
        self._agent_mod = _import_from(agent_py, "ours_agent")
        self._model, agent_tok, self._device = self._agent_mod.load(self.ckpt, tokenizer=str(tok_json))
        from tokenizers import Tokenizer

        self._tok = Tokenizer.from_file(str(tok_json))

    def tokenizer(self):
        self._load()
        outer = self

        class _T:
            def count(self, text: str) -> int:
                return len(outer._tok.encode(text).ids)

        return _T()

    def _prompt_ids(self, messages, tools=None):
        text = self._render(_to_ours(messages), tools=_flat_tools())
        return self._tok.encode(text + GEN_PROMPT_SUFFIX).ids

    def count_context(self, messages: list[dict[str, Any]]) -> int:
        self._load()
        return len(self._prompt_ids(messages))

    def generate(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
        max_tokens: int = 256,
        temperature: float = 0.0,
        seed: Optional[int] = None,
    ) -> BackendReply:
        self._load()
        ids = self._prompt_ids(messages, tools)
        out_ids = self._agent_mod.generate(
            self._model,
            self._tok,
            ids,
            self._device,
            max_new=max_tokens,
            temp=temperature,
        )
        if out_ids and out_ids[: len(ids)] == ids:
            out_ids = out_ids[len(ids):]
        # keep special tokens: <|tool_call|> is one, and the adapter parses it
        return BackendReply(text=self._tok.decode(out_ids, skip_special_tokens=False).split("<|im_end|>")[0])
