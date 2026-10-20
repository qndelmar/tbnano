"""The fixed tool set (spec section 3).

Tools are declared in OpenAI function format; each format adapter renders
them into the target model's native call syntax. The sandbox executes them.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "run",
            "description": (
                "Run a bash command (`bash -lc`, cwd=/task, empty stdin, "
                "10s timeout). No interactive programs (vim, less, REPLs); "
                "no network. Returns exit code and output."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "cmd": {"type": "string", "description": "Command to run."},
                },
                "required": ["cmd"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a slice of a text file under /task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "start": {"type": "integer", "description": "1-based first line.", "default": 1},
                    "lines": {"type": "integer", "description": "Max lines to read.", "default": 60},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write (overwrite) a text file under /task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "finish",
            "description": (
                "End the episode. Pass your answer in `answer` when the task "
                "asks for one (e.g. a number). Otherwise call with no answer."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {"type": "string", "default": ""},
                },
            },
        },
    },
]

TOOL_NAMES = {t["function"]["name"] for t in TOOL_SCHEMAS}

# Compact text description of the tools for non-native (tag-based) formats.
# Kept minimal: it must fit the <=600 token system-prompt budget together
# with usage rules.
TOOLS_BRIEF = """\
You operate in a Linux terminal via tool calls. Available tools:

run(cmd: str) -> {exit_code, stdout, stderr}
    Run `bash -lc cmd` in /task, empty stdin, 10s timeout. No interactive
    programs (vim, less, REPLs), no network.
read_file(path: str, start: int = 1, lines: int = 60) -> {text, total_lines}
write_file(path: str, content: str) -> {ok, bytes}
finish(answer: str = "")
    End the episode. `answer` is required when the task asks for a value.

Rules: exactly one tool call per reply. Output too long is truncated with
"... [N lines cut] ...". Reply without a tool call only if you cannot act.
"""


@dataclass
class ToolCall:
    """A canonical parsed tool call."""

    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    raw: str = ""

    def to_json(self) -> str:
        return json.dumps({"name": self.name, "arguments": self.arguments})
