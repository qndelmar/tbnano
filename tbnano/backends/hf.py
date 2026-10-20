"""HF-style backends: transformers (default), mlx-lm, or vllm.

The chat template comes from the model's own tokenizer
(`tokenizer.apply_chat_template`) — the one place where tbnano sees the
model (spec 3). For the `lfm_pythonic`/`hermes` formats the OpenAI tool
schemas are passed to the template via `tools=` plus a short system
prompt (review P2-13); when a template cannot render that, we fall back
to no-tools rendering once and the adapter still parses the raw text —
the fallback is recorded in `self.template_fallback` for the report.

Tool results are injected as role=tool messages; if the model's
template lacks a tool role, they are folded into a user turn.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Optional

from ..tokens import HFTokenizer, Tokenizer
from .base import BackendReply

# Formats whose chat template understands OpenAI tool schemas.
_TOOLS_FMTS = {"lfm_pythonic", "hermes", "qwen_xml", "openai"}

_TOOL_SYSTEM = (
    "You are a terminal agent. Reply with exactly one tool call using the "
    "provided functions; never answer in plain text."
)


_GEN_KEYS = ("temperature", "top_k", "top_p", "min_p", "repetition_penalty")


def _generation_config(model_id: str) -> dict[str, Any]:
    """The sampling settings the model's authors ship in generation_config.json."""
    import json

    from huggingface_hub import hf_hub_download

    try:
        cfg = json.loads(Path(hf_hub_download(model_id, "generation_config.json")).read_text())
    except Exception:
        return {}
    return {k: cfg[k] for k in _GEN_KEYS if cfg.get(k) is not None}


class HFBackend:
    name = "hf"

    def __init__(
        self,
        model_id: str,
        impl: str = "transformers",
        fmt: str = "json_tags",
        device: Optional[str] = None,
        load_kwargs: Optional[dict] = None,
        sampling: str = "greedy",
        flat_tools: bool = False,
    ):
        self.model_id = model_id
        self.sampling = sampling
        self.flat_tools = flat_tools
        self.gen_cfg: dict[str, Any] = {}
        self.impl = impl
        self.fmt = fmt
        # the chat template gets tools= and lists the schemas itself
        self.renders_tools = fmt in _TOOLS_FMTS
        self.device = device
        self.load_kwargs = load_kwargs or {}
        self.template_fallback = False  # set when tools= is unsupported
        self.max_context: Optional[int] = None
        self._model = None
        self._tok_hf = None
        self._loaded = False

    # -- loading ------------------------------------------------------
    def _load(self) -> None:
        if self._loaded:
            return
        if self.impl == "mlx":
            try:
                from mlx_lm import load as mlx_load
            except ImportError as e:
                raise ImportError(
                    "mlx backend needs mlx-lm: pip install mlx-lm (Apple "
                    "silicon only)"
                ) from e
            self._model, self._tok_hf = mlx_load(self.model_id)
        else:
            from transformers import AutoTokenizer

            self._tok_hf = AutoTokenizer.from_pretrained(
                self.model_id, trust_remote_code=True
            )
        if self.impl == "transformers":
            from transformers import AutoModelForCausalLM

            kwargs = dict(self.load_kwargs)
            kwargs.setdefault("dtype", "auto")
            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_id, trust_remote_code=True, **kwargs
            )
            if self.device:
                self._model = self._model.to(self.device)
            else:
                try:
                    import torch

                    if torch.cuda.is_available():
                        self._model = self._model.to("cuda")
                except ImportError:
                    pass
        elif self.impl == "vllm":
            try:
                from vllm import LLM
            except ImportError as e:
                raise ImportError(
                    "vllm backend needs vllm; alternatively serve the model "
                    "with `vllm serve <model>` and use "
                    "--backend openai --model api:<name> "
                    "--base-url http://localhost:8000/v1"
                ) from e
            kw = dict(self.load_kwargs)
            kw.setdefault("gpu_memory_utilization", 0.85)
            self._model = LLM(model=self.model_id, **kw)
        if self.sampling == "model":
            self.gen_cfg = _generation_config(self.model_id)
            print(f"[tbnano] {self.model_id}: sampling from generation_config {self.gen_cfg}",
                  file=sys.stderr)
        try:
            mc = getattr(getattr(self._model, "config", None),
                         "max_position_embeddings", None)
            if mc and mc < 10**9:
                self.max_context = int(mc)
        except Exception:
            pass
        self._loaded = True

    def tokenizer(self) -> Tokenizer:
        self._load()
        return HFTokenizer(self._tok_hf)

    # -- rendering ----------------------------------------------------
    def _render(self, messages: list[dict[str, Any]]) -> str:
        kwargs: dict[str, Any] = {
            # enable_thinking=False: hybrid-reasoning templates (Qwen3.x) would
            # otherwise spend the 256-token reply budget on <think>; templates
            # without the variable ignore it
            "tokenize": False, "add_generation_prompt": True, "enable_thinking": False,
        }
        if self.fmt in _TOOLS_FMTS:
            from ..tools import TOOL_SCHEMAS

            kwargs["tools"] = ([t["function"] for t in TOOL_SCHEMAS] if self.flat_tools
                               else TOOL_SCHEMAS)
            if not any(m.get("role") == "system" for m in messages):
                messages = [{"role": "system", "content": _TOOL_SYSTEM}] + list(
                    messages
                )
        try:
            return self._tok_hf.apply_chat_template(messages, **kwargs)
        except Exception:
            pass
        # Fallback 1: template does not accept tools= (log once; the
        # adapter still parses the raw text reply).
        if "tools" in kwargs and not self.template_fallback:
            self.template_fallback = True
            print(
                f"[tbnano] {self.model_id}: chat template does not accept "
                f"tools=; rendering without tool schemas",
                file=sys.stderr,
            )
        kwargs.pop("tools", None)
        try:
            return self._tok_hf.apply_chat_template(messages, **kwargs)
        except Exception:
            pass
        # Fallback 2: template without a `tool` role — fold tool results
        # into user turns.
        fixed = []
        for m in messages:
            if m.get("role") == "tool":
                fixed.append(
                    {"role": "user", "content": "TOOL RESULT: " + m["content"]}
                )
            else:
                fixed.append(m)
        return self._tok_hf.apply_chat_template(fixed, **kwargs)

    def count_context(self, messages: list[dict[str, Any]]) -> int:
        self._load()
        try:
            return len(self._tok_hf.encode(self._render(messages)))
        except Exception:
            tok = HFTokenizer(self._tok_hf)
            return sum(
                tok.count(str(m.get("content") or "")) + 8 for m in messages
            )

    # -- generation ----------------------------------------------------
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
        if self.impl == "mlx":
            from mlx_lm import generate as mlx_generate
            from mlx_lm.sample_utils import make_logits_processors, make_sampler

            g = self.gen_cfg
            if g:
                import mlx.core as mx

                mx.random.seed(seed or 0)
                sampler = make_sampler(temp=g.get("temperature", 1.0), top_p=g.get("top_p", 0.0) or 0.0,
                                       min_p=g.get("min_p", 0.0) or 0.0, top_k=g.get("top_k", 0) or 0)
                procs = make_logits_processors(repetition_penalty=g.get("repetition_penalty"))
            else:
                sampler, procs = make_sampler(temp=max(temperature, 1e-5)), None
            text = mlx_generate(
                self._model,
                self._tok_hf,
                prompt=prompt,
                max_tokens=max_tokens,
                sampler=sampler,
                logits_processors=procs,
                verbose=False,
            )
            return BackendReply(text=text)
        if self.impl == "vllm":
            from vllm import SamplingParams

            sp = SamplingParams(
                max_tokens=max_tokens,
                temperature=temperature,
                seed=seed,
            )
            out = self._model.generate([prompt], sp)
            return BackendReply(text=out[0].outputs[0].text)
        # transformers
        import torch

        ids = self._tok_hf(prompt, return_tensors="pt").to(self._model.device)
        gen_kwargs: dict[str, Any] = {
            "max_new_tokens": max_tokens,
            "do_sample": temperature > 0,
            "temperature": temperature if temperature > 0 else 1.0,
            "pad_token_id": self._tok_hf.eos_token_id,
        }
        if self.gen_cfg:
            gen_kwargs.update({"do_sample": True, **{k: v for k, v in self.gen_cfg.items()
                                                     if k != "min_p" or v}})
        if seed is not None:
            torch.manual_seed(seed)
        with torch.no_grad():
            out = self._model.generate(**ids, **gen_kwargs)
        text = self._tok_hf.decode(
            out[0][ids["input_ids"].shape[1]:], skip_special_tokens=False
        )
        return BackendReply(text=text, usage_tokens=len(out[0]))
