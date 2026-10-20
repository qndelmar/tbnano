"""tbnano — TerminalBench Nano.

A tool-calling-in-terminal benchmark for small models (50M-1B) with an
episode context budget of <=8192 tokens. Inspired by TerminalBench 1.0:
task directories + pytest verification + reference solutions, but with a
fixed tool API instead of raw tmux and hard per-task budgets.
"""

__version__ = "0.1.0"
