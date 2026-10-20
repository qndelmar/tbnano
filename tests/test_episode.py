"""Episode loop: end reasons, budgets, two-text-termination."""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

from tbnano.adapters import get_adapter
from tbnano.backends.scripted import ScriptedBackend
from tbnano.episode import run_episode
from tbnano.sandbox.local import LocalSandbox
from tbnano.tasksio import TaskSpec
from tbnano.tokens import ApproxTokenizer

TOK = ApproxTokenizer()


def make_spec(tmp: Path, max_turns=6, instruction="do it") -> TaskSpec:
    d = tmp / "t"
    (d / "setup").mkdir(parents=True, exist_ok=True)
    (d / "tests").mkdir(exist_ok=True)
    (d / "task.yaml").write_text(
        yaml.safe_dump(
            {
                "id": "t",
                "level": 1,
                "category": "x",
                "instruction": instruction,
                "answer_mode": "files",
                "max_turns": max_turns,
            }
        )
    )
    return TaskSpec(
        id="t", dir=d, level=1, category="x", instruction=instruction,
        max_turns=max_turns,
    )


@pytest.fixture
def sandbox(tmp_path):
    (tmp_path / "t" / "setup").mkdir(parents=True, exist_ok=True)
    (tmp_path / "t" / "tests").mkdir(exist_ok=True)
    sb = LocalSandbox(work_root=tmp_path / "sb")
    sb.start(tmp_path / "t" / "setup", "t")
    yield sb
    sb.close()


def test_finish_end(tmp_path, sandbox):
    spec = make_spec(tmp_path)
    b = ScriptedBackend(script="quitter")
    ep = run_episode(spec, b, get_adapter("json_tags"), sandbox, TOK)
    assert ep.end_reason == "finish"
    assert ep.turns_used == 1


def test_two_texts_end_no_call(tmp_path, sandbox):
    spec = make_spec(tmp_path)
    replies = tmp_path / "replies.txt"
    replies.write_text("hmm let me think\nstill thinking\n")
    b = ScriptedBackend(script=f"file:{replies}")
    ep = run_episode(spec, b, get_adapter("json_tags"), sandbox, TOK)
    assert ep.end_reason == "no_call"
    assert ep.turns_used == 2
    assert ep.answer == ""


def test_max_turns(tmp_path, sandbox):
    spec = make_spec(tmp_path, max_turns=3)
    replies = tmp_path / "replies.txt"
    # valid run call each time, never finishes
    replies.write_text(
        ('<|tool_call|>{"name":"run","arguments":{"cmd":"true"}}'
         "<|tool_call_end|>\n") * 5
    )
    b = ScriptedBackend(script=f"file:{replies}")
    ep = run_episode(spec, b, get_adapter("json_tags"), sandbox, TOK,
                     loop_stop=False)
    assert ep.end_reason == "max_turns"
    assert ep.turns_used == 3


def test_loop_stop(tmp_path, sandbox):
    """3 identical consecutive calls end the episode (spec v2 3)."""
    spec = make_spec(tmp_path, max_turns=6)
    replies = tmp_path / "replies.txt"
    replies.write_text(
        ('<|tool_call|>{"name":"run","arguments":{"cmd":"true"}}'
         "<|tool_call_end|>\n") * 5
    )
    b = ScriptedBackend(script=f"file:{replies}")
    ep = run_episode(spec, b, get_adapter("json_tags"), sandbox, TOK)
    assert ep.end_reason == "loop"
    assert ep.turns_used == 3


def test_loop_stop_different_calls(tmp_path, sandbox):
    """Different calls in between break the streak."""
    spec = make_spec(tmp_path, max_turns=6)
    replies = tmp_path / "replies.txt"
    one = ('<|tool_call|>{"name":"run","arguments":{"cmd":"true"}}'
           "<|tool_call_end|>")
    two = ('<|tool_call|>{"name":"run","arguments":{"cmd":"ls"}}'
           "<|tool_call_end|>")
    fin = ('<|tool_call|>{"name":"finish","arguments":{"answer":""}}'
           "<|tool_call_end|>")
    replies.write_text("\n".join([one, one, two, one, one, one, fin]))
    b = ScriptedBackend(script=f"file:{replies}")
    ep = run_episode(spec, b, get_adapter("json_tags"), sandbox, TOK)
    assert ep.end_reason == "loop"  # 3x same after the interrupt
    assert ep.turns_used == 6


def test_invalid_call_counts(tmp_path, sandbox):
    spec = make_spec(tmp_path)
    replies = tmp_path / "replies.txt"
    replies.write_text(
        "<|tool_call|>{bad json}<|tool_call_end|>\n"
        '<|tool_call|>{"name":"finish","arguments":{"answer":"ok"}}'
        "<|tool_call_end|>\n"
    )
    b = ScriptedBackend(script=f"file:{replies}")
    ep = run_episode(spec, b, get_adapter("json_tags"), sandbox, TOK)
    assert ep.end_reason == "finish"
    assert ep.invalid_calls == 1
    assert ep.answer == "ok"


def test_context_overflow(tmp_path, sandbox):
    # Instruction alone exceeding the context budget ends immediately.
    spec = make_spec(tmp_path, instruction="x " * 40000)
    b = ScriptedBackend(script="quitter")
    ep = run_episode(spec, b, get_adapter("json_tags"), sandbox, TOK)
    assert ep.end_reason == "context_overflow"


def test_oracle_probe_finish(tmp_path, sandbox):
    spec = make_spec(tmp_path)
    b = ScriptedBackend(script="oracle")
    b.set_oracle(["echo 7 > answer.txt"])
    ep = run_episode(spec, b, get_adapter("json_tags"), sandbox, TOK)
    assert ep.end_reason == "finish"
    assert ep.answer == "7"
