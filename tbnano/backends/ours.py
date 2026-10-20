"""Backend for our own checkpoints (`ckpt:<path>`).

Spec 3/7: for our models the chat template is `render()` from
`chat_format.py` in our training repo, and inference is a wrapper over
`agent.py` exposing `load()` / `generate()`. Point tbnano at that repo
with TBNANO_OURS_REPO (default: sibling dir `../small-test-llm`).
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Any, Optional

from ..tokens import ApproxTokenizer, Tokenizer
from .base import BackendReply


def _import_from(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class OursBackend:
    name = "ours"

    def __init__(self, ckpt: str, repo: Optional[str] = None, **_):
        self.ckpt = ckpt
        self.repo = Path(
            repo or os.environ.get("TBNANO_OURS_REPO", "../small-test-llm")
        ).resolve()
        self._agent = None
        self._render = None
        self._tok = None

    def _load(self) -> None:
        if self._agent is not None:
            return
        agent_py = self.repo / "agent.py"
        fmt_py = self.repo / "chat_format.py"
        if not agent_py.exists() or not fmt_py.exists():
            raise FileNotFoundError(
                f"ours backend needs agent.py and chat_format.py in "
                f"{self.repo} (set TBNANO_OURS_REPO)"
            )
        fmt = _import_from(fmt_py, "ours_chat_format")
        self._render = fmt.render
        agent = _import_from(agent_py, "ours_agent")
        self._agent = agent.load(self.ckpt)
        tok_mod = self.repo / "tokenizer.py"
        if tok_mod.exists():
            self._tok = _import_from(tok_mod, "ours_tokenizer")

    def tokenizer(self) -> Tokenizer:
        self._load()
        outer = self

        class _T:
            def count(self, text: str) -> int:
                if outer._tok is not None and hasattr(outer._tok, "encode"):
                    return len(outer._tok.encode(text))
                return ApproxTokenizer().count(text)

        return _T()

    def count_context(self, messages: list[dict[str, Any]]) -> int:
        self._load()
        try:
            return self.tokenizer().count(self._render(messages))
        except Exception:
            return super_count(self, messages)

    def generate(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
        max_tokens: int = 256,
        temperature: float = 0.0,
        seed: Optional[int] = None,
    ) -> BackendReply:
        self._load()
        prompt = self._render(messages)
        text = self._agent.generate(
            prompt, max_tokens=max_tokens, temperature=temperature, seed=seed
        )
        return BackendReply(text=text)


def super_count(backend: OursBackend, messages) -> int:
    tok = backend.tokenizer()
    return sum(tok.count(str(m.get("content") or "")) + 8 for m in messages)
