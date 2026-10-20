"""Model backends: one interface `generate(messages, tools) -> BackendReply`.

Spec section 7: pluggable backends — hf/mlx/vllm/transformers, ours
(ckpt: checkpoints), api (OpenAI-compatible). `scripted` is a fake backend
used by tbnano's own tests and by --agent oracle/quitter validation runs.
"""

from __future__ import annotations

from .base import Backend, BackendReply
from .scripted import ScriptedBackend


def make_backend(
    model: str,
    backend: str = "auto",
    tokenizer=None,
    **kwargs,
) -> Backend:
    """Route --model/--backend to an implementation.

    model forms: hf:<repo>, ckpt:<path>, api:<model>, scripted:<script>
    backend:   transformers | vllm | mlx | ours | openai | scripted | auto
    """
    kind, _, value = model.partition(":")

    if backend == "auto":
        backend = {
            "hf": "transformers",
            "ckpt": "ours",
            "api": "openai",
            "scripted": "scripted",
        }.get(kind, kind if kind in ("transformers", "vllm", "mlx") else "scripted")

    if backend == "scripted":
        return ScriptedBackend(script=value if kind == "scripted" else model, **kwargs)
    if backend in ("transformers", "vllm", "mlx"):
        from .hf import HFBackend

        return HFBackend(model_id=value if kind == "hf" else model,
                         impl=backend, **kwargs)
    if backend == "ours":
        from .ours import OursBackend

        return OursBackend(ckpt=value if kind == "ckpt" else model, **kwargs)
    if backend == "openai":
        from .api import APIBackend

        return APIBackend(model=value if kind == "api" else model, **kwargs)
    raise ValueError(f"unknown backend {backend!r}")


__all__ = ["Backend", "BackendReply", "ScriptedBackend", "make_backend"]
