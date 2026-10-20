"""Token counting.

The spec says context is counted "with the evaluated model's tokenizer".
This module provides the counting abstraction used everywhere in tbnano:

- `Tokenizer` protocol: anything with ``count(text) -> int``.
- `ApproxTokenizer`: char-based approximation (~4 chars/token). Used when
  the model's tokenizer is unavailable — e.g. `tbnano validate`, which
  must work without loading model weights. It is deliberately used for
  budget *validation* only; a real run counts with the model's tokenizer.
- `HFTokenizer`: wraps a transformers tokenizer.
- `TiktokenTokenizer`: for API models where the real tokenizer is remote.
"""

from __future__ import annotations

from typing import Protocol


class Tokenizer(Protocol):
    def count(self, text: str) -> int: ...


class ApproxTokenizer:
    """~4 chars per token approximation. Conservative for code/logs."""

    CHARS_PER_TOKEN = 4.0

    def count(self, text: str) -> int:
        return max(1, int(len(text) / self.CHARS_PER_TOKEN) + 1)


class HFTokenizer:
    def __init__(self, hf_tokenizer):
        self._tok = hf_tokenizer

    def count(self, text: str) -> int:
        return len(self._tok.encode(text))


class TiktokenTokenizer:
    def __init__(self, model: str = "gpt-4o-mini"):
        import tiktoken

        try:
            self._enc = tiktoken.encoding_for_model(model)
        except Exception:
            self._enc = tiktoken.get_encoding("o200k_base")

    def count(self, text: str) -> int:
        return len(self._enc.encode(text))


def approx_tokens(text: str) -> int:
    """Module-level convenience for places without a configured tokenizer."""
    return ApproxTokenizer().count(text)
