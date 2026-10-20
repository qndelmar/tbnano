"""Regression tests for the review fixes:

- tests/ are never visible inside the sandbox during the episode
- malformed tool args → nudge + invalid_calls, never an exception
- --sandbox local with a non-scripted backend requires --unsafe-local
- context is re-checked after every appended message
- partial metric ignores presence tests; harness_error counted
"""

import json
import tempfile
from pathlib import Path

import pytest

from tbnano.adapters import get_adapter
from tbnano.backends.scripted import ScriptedBackend
from tbnano.episode import run_episode
from tbnano.sandbox.local import LocalSandbox
from tbnano.tasksio import TaskSpec
from tbnano.tokens import ApproxTokenizer

TOK = ApproxTokenizer()


def make_spec(tmp: Path, max_turns=8) -> TaskSpec:
    d = tmp / "t"
    (d / "setup").mkdir(parents=True, exist_ok=True)
    (d / "tests").mkdir(exist_ok=True)
    (d / "tests" / "test.py").write_text("def test_x():\n    assert True\n")
    return TaskSpec(
        id="t", dir=d, level=1, category="x", instruction="do it",
        max_turns=max_turns,
    )


def make_sandbox(tmp: Path) -> LocalSandbox:
    sb = LocalSandbox(work_root=tmp / "sb")
    sb.start(tmp / "t" / "setup", "t")
    return sb


def test_tests_not_visible_in_sandbox(tmp_path):
    spec = make_spec(tmp_path)
    sb = make_sandbox(tmp_path)
    try:
        # no tests dir, no test.py, no pytest paths anywhere under /task
        found = [str(p) for p in sb.task_dir.rglob("*") if "test" in p.name]
        assert found == [], f"tests leaked into sandbox: {found}"
        res = sb.run("find /task -name 'test*' | head", timeout=10)
        assert "test.py" not in res.stdout
    finally:
        sb.close()


def test_tests_staged_only_in_run_tests(tmp_path):
    spec = make_spec(tmp_path)
    sb = make_sandbox(tmp_path)
    try:
        tr = sb.run_tests(tmp_path / "t" / "tests", timeout=30.0)
        assert tr.total == 1 and tr.passed == 1
    finally:
        sb.close()


def _scripted_lines(tmp_path, replies):
    f = tmp_path / "script.txt"
    f.write_text("\n".join(replies))
    return ScriptedBackend(script=f"file:{f}")


def _call(name, args):
    return "<|tool_call|>" + json.dumps({"name": name, "arguments": args}) \
        + "<|tool_call_end|>"


def test_malformed_args_increment_invalid_no_crash(tmp_path):
    spec = make_spec(tmp_path)
    sb = make_sandbox(tmp_path)
    replies = [
        _call("run", {"cmd": 123}),          # wrong type -> invalid
        _call("run", "ls"),                  # non-dict -> invalid
        _call("bogus_tool", {}),             # unknown tool
        _call("run", {"cmd": "echo hi"}),    # valid
        _call("finish", {"answer": ""}),
    ]
    b = _scripted_lines(tmp_path, replies)
    ep = run_episode(spec, b, get_adapter("json_tags"), sb, TOK)
    try:
        assert ep.end_reason == "finish"
        assert ep.invalid_calls >= 2
        # nudges were appended as tool messages (trajectory marks kind=invalid)
        kinds = [t.get("kind") for t in ep.trajectory]
        assert "invalid" in kinds
    finally:
        sb.close()


def test_wrong_scalar_types_coerced(tmp_path):
    spec = make_spec(tmp_path)
    sb = make_sandbox(tmp_path)
    replies = [
        _call("read_file", {"path": "x.txt", "lines": "10"}),  # str->int ok
        _call("finish", {"answer": ""}),
    ]
    b = _scripted_lines(tmp_path, replies)
    ep = run_episode(spec, b, get_adapter("json_tags"), sb, TOK)
    try:
        assert ep.end_reason == "finish"
        assert ep.invalid_calls == 0
    finally:
        sb.close()


def test_unsafe_local_gate_refuses(tmp_path, capsys):
    from tbnano.cli import main

    rc = main([
        "run", "--model", "hf:foo/bar", "--backend", "transformers",
        "--sandbox", "local", "--tasks", str(tmp_path), "--n", "1",
    ])
    out = capsys.readouterr()
    assert rc == 2
    assert "unsafe-local" in out.err


def test_unsafe_local_gate_allows_scripted(tmp_path):
    # scripted agents (oracle/quitter validation) may use local sandbox
    from tbnano.cli import main

    tasks = tmp_path / "tasks"
    spec_dir = tasks / "task1"
    (spec_dir / "setup").mkdir(parents=True)
    (spec_dir / "tests").mkdir()
    (spec_dir / "task.yaml").write_text(
        "id: task1\nlevel: 1\ncategory: x\ninstruction: noop\n"
        "answer_mode: files\nmax_turns: 3\n")
    (spec_dir / "tests" / "test.py").write_text("def test_ok():\n    assert True\n")
    rc = main([
        "run", "--agent", "quitter", "--sandbox", "local",
        "--tasks", str(tasks), "--out", str(tmp_path / "runs"),
    ])
    assert rc == 0


def test_partial_ignores_presence_tests():
    from tbnano.sandbox.base import TestResult

    tr = TestResult(total=4, passed=3, presence_passed=1, presence_total=1)
    # 2 of 3 real tests passed -> partial 2/3, not 3/4
    assert abs(tr.partial - 2 / 3) < 1e-9


def test_harness_error_end_reason(tmp_path, monkeypatch):
    spec = make_spec(tmp_path)
    sb = make_sandbox(tmp_path)
    b = ScriptedBackend(script="quitter")

    def boom(*a, **kw):
        raise RuntimeError("kaboom")

    monkeypatch.setattr(b, "generate", boom)
    ep = run_episode(spec, b, get_adapter("json_tags"), sb, TOK)
    try:
        assert ep.end_reason == "harness_error"
    finally:
        sb.close()


def test_zero_tests_is_an_error(tmp_path):
    from tbnano.sandbox.base import finalize_test_result
    tr = finalize_test_result("no module named pytest\n", 0)
    assert tr.error and not tr.resolved


def test_resume_skips_finished_and_reruns_partial(tmp_path, capsys):
    # after a crash: finished trajectories are reused, half-written ones re-run
    from tbnano.cli import main

    tasks = tmp_path / "tasks"
    for tid in ("task1", "task2"):
        d = tasks / tid
        (d / "setup").mkdir(parents=True)
        (d / "tests").mkdir()
        (d / "task.yaml").write_text(
            f"id: {tid}\nlevel: 1\ncategory: x\ninstruction: noop\n"
            "answer_mode: files\nmax_turns: 3\n")
        (d / "tests" / "test.py").write_text("def test_ok():\n    assert True\n")
    args = ["run", "--agent", "quitter", "--sandbox", "local",
            "--tasks", str(tasks), "--out", str(tmp_path / "runs")]
    assert main(args) == 0
    out_dir = next((tmp_path / "runs").iterdir())
    t1 = (out_dir / "task1.jsonl").read_text()
    (out_dir / "task2.jsonl").write_text('{"turn": 0}\n')  # crash mid-episode
    capsys.readouterr()
    assert main(args + ["--resume"]) == 0
    assert "resume: 1 done, 1 to run" in capsys.readouterr().out
    assert (out_dir / "task1.jsonl").read_text() == t1
    assert json.loads((out_dir / "task2.jsonl").read_text().splitlines()[-1])["summary"]
    rep = json.loads((out_dir / "report.json").read_text())
    assert rep["overall"]["n"] == 2


def test_text_final_ends_episode_with_text_answer(tmp_path):
    # --final-answer text: LFM2.5-style plain-text final answer after a tool result
    spec = make_spec(tmp_path)
    sb = make_sandbox(tmp_path)
    b = _scripted_lines(tmp_path, [_call("run", {"cmd": "echo 42"}), "The sum is 42."])
    try:
        ep = run_episode(spec, b, get_adapter("json_tags"), sb, TOK, text_final=True)
        assert ep.end_reason == "finish"
        assert ep.answer == "The sum is 42."
        assert [t["kind"] for t in ep.trajectory] == ["call", "final_text"]
    finally:
        sb.close()


def test_text_final_default_off_still_nudges(tmp_path):
    spec = make_spec(tmp_path)
    sb = make_sandbox(tmp_path)
    b = _scripted_lines(tmp_path, ["hello", "still text"])
    try:
        ep = run_episode(spec, b, get_adapter("json_tags"), sb, TOK)
        assert ep.end_reason == "no_call"
    finally:
        sb.close()


def test_text_final_system_prompt():
    from tbnano.tools import FINAL_TEXT, FINAL_TOOL

    ad = get_adapter("lfm_pythonic")
    for tmpl in (True, False):
        p = ad.system_prompt(schemas_in_template=tmpl, text_final=True)
        assert "plain text with no tool call" in p
        assert FINAL_TOOL not in p
    assert FINAL_TOOL in ad.system_prompt(schemas_in_template=True)


def test_binary_stdout_does_not_crash_episode(tmp_path):
    # `cat data.db` on a sqlite file used to raise UnicodeDecodeError -> harness_error
    spec = make_spec(tmp_path)
    (tmp_path / "t" / "setup" / "blob.bin").write_bytes(b"SQLite format 3\x00\x99\xff\xfe")
    sb = make_sandbox(tmp_path)
    b = _scripted_lines(tmp_path, [_call("run", {"cmd": "cat blob.bin"}), _call("finish", {"answer": ""})])
    try:
        ep = run_episode(spec, b, get_adapter("json_tags"), sb, TOK)
        assert ep.end_reason == "finish"
        assert "�" in ep.trajectory[0]["result"] or "\\ufffd" in ep.trajectory[0]["result"]
    finally:
        sb.close()
