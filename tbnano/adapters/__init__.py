"""Format adapters: translate the canonical tool API into each model's
native call format and parse model replies back into canonical calls."""

from __future__ import annotations

from .base import Adapter, ParseResult, ParseStatus
from .hermes import HermesAdapter
from .json_tags import JsonTagsAdapter
from .lfm_pythonic import LfmPythonicAdapter
from .openai import OpenAIAdapter
from .qwen_xml import QwenXmlAdapter

_ADAPTERS = {
    JsonTagsAdapter.name: JsonTagsAdapter,
    LfmPythonicAdapter.name: LfmPythonicAdapter,
    HermesAdapter.name: HermesAdapter,
    OpenAIAdapter.name: OpenAIAdapter,
    QwenXmlAdapter.name: QwenXmlAdapter,
}


def get_adapter(name: str) -> Adapter:
    try:
        return _ADAPTERS[name]()
    except KeyError:
        raise ValueError(
            f"unknown format adapter {name!r}; available: {sorted(_ADAPTERS)}"
        ) from None


__all__ = [
    "Adapter",
    "ParseResult",
    "ParseStatus",
    "get_adapter",
]
