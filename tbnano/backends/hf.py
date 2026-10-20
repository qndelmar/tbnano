"""HuggingFace backend: transformers (default), vllm, or mlx-lm.

The chat template comes from the model's own tokenizer
(`tokenizer.apply_chat_template`) — the one place where tbnano sees the
model, per spec 3. Tool results are injected as role=tool messages; if
the model's template lacks a tool role, they are folded into a user turn.
"""

from __future__ import annotations

from typing import Any, Optional

from ..tokens import HFTokenizer, Tokenizer
from .base import BackendReply


class HFBackend:
    name = "hf"

    def __init__(
        self,
        model_id: str,
        impl: str = "transformers",
        device: Optional[str] = None,
        load_kwargs: Optional[dict] = None,
    ):
        self.model_id = model_id
        self.impl = impl
        self.device = device
        self.load_kwargs = load_kwargs or {}
        self._model = None
        self._tok_hf = None
        self._loaded = False

    def _load(self) -> None:
        if self._loaded:
            return
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self._tok_hf = AutoTokenizer.from_pretrained(
            self.model_id, trust_remote_code=True
        )
        kwargs = dict(self.load_kwargs)
        kwargs.setdefault("dtype", "auto")
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_id, trust_remote_code=True, **kwargs
        )
        if self.device:
            self._model = self._model.to(self.device)
        elif self.impl == "transformers":
            try:
                import torch

                if torch.cuda.is_available():
                    self._model = self._model.to("cuda")
            except ImportError:
                pass
        if self.impl == "mlx":
            raise NotImplementedError(
                "mlx impl: use mlx-lm's load()/generate() — not wired in "
                "this environment; transformers works for the same models"
            )
        if self.impl == "vllm":
            raise NotImplementedError(
                "vllm impl: serve the model and point the api backend at it "
                "(--model api:<name> --base-url http://localhost:8000/v1)"
            )
        self._loaded = True

    def tokenizer(self) -> Tokenizer:
        self._load()
        return HFTokenizer(self._tok_hf)

    def count_context(self, messages: list[dict[str, Any]]) -> int:
        self._load()
        try:
            text = self._tok_hf.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            return len(self._tok_hf.encode(text))
        except Exception:
            return super_count_context(self, messages)

    def generate(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
        max_tokens: int = 256,
        temperature: float = 0.0,
        seed: Optional[int] = None,
    ) -> BackendReply:
        self._load()
        import torch

        prompt = self._render(messages)
        ids = self._tok_hf(prompt, return_tensors="pt").to(self._model.device)
        gen_kwargs: dict[str, Any] = {
            "max_new_tokens": max_tokens,
            "do_sample": temperature > 0,
            "temperature": temperature if temperature > 0 else 1.0,
            "pad_token_id": self._tok_hf.eos_token_id,
        }
        if seed is not None:
            torch.manual_seed(seed)
        with torch.no_grad():
            out = self._model.generate(**ids, **gen_kwargs)
        text = self._tok_hf.decode(
            out[0][ids["input_ids"].shape[1]:], skip_special_tokens=False
        )
        return BackendReply(text=text, usage_tokens=len(out[0]))

    def _render(self, messages: list[dict[str, Any]]) -> str:
        try:
            return self._tok_hf.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        except Exception:
            # Template without a `tool` role: fold tool results into user.
            fixed = []
            for m in messages:
                if m.get("role") == "tool":
                    fixed.append(
                        {"role": "user", "content": "TOOL RESULT: " + m["content"]}
                    )
                else:
                    fixed.append(m)
            return self._tok_hf.apply_chat_template(
                fixed, tokenize=False, add_generation_prompt=True
            )


def super_count_context(backend: HFBackend, messages) -> int:
    tok = backend.tokenizer()
    return sum(tok.count(str(m.get("content") or "")) + 8 for m in messages)
