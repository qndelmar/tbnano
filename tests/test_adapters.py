"""Adapter parsing tests — each format's markup, errors, unknown tools."""

import pytest

from tbnano.adapters import get_adapter
from tbnano.adapters.base import ParseStatus


def test_json_tags_valid():
    a = get_adapter("json_tags")
    r = a.parse('<|tool_call|>{"name": "run", "arguments": {"cmd": "ls"}}'
                "<|tool_call_end|>")
    assert r.status is ParseStatus.CALL
    assert r.call.name == "run"
    assert r.call.arguments == {"cmd": "ls"}


def test_json_tags_text():
    a = get_adapter("json_tags")
    r = a.parse("let me think about this")
    assert r.status is ParseStatus.TEXT


def test_json_tags_bad_json_is_invalid():
    a = get_adapter("json_tags")
    r = a.parse("<|tool_call|>{not json}<|tool_call_end|>")
    assert r.status is ParseStatus.INVALID
    assert "JSON" in r.error


def test_json_tags_unknown_tool():
    a = get_adapter("json_tags")
    r = a.parse('<|tool_call|>{"name": "shell", "arguments": {}}'
                "<|tool_call_end|>")
    assert r.status is ParseStatus.INVALID


def test_json_tags_unterminated():
    a = get_adapter("json_tags")
    r = a.parse('<|tool_call|>{"name": "run"')
    assert r.status is ParseStatus.INVALID


def test_lfm_pythonic_valid():
    a = get_adapter("lfm_pythonic")
    r = a.parse('<|tool_call_start|>[run(cmd="ls -la")]<|tool_call_end|>')
    assert r.status is ParseStatus.CALL
    assert r.call.name == "run"
    assert r.call.arguments == {"cmd": "ls -la"}


def test_lfm_pythonic_read_file_args():
    a = get_adapter("lfm_pythonic")
    r = a.parse(
        '<|tool_call_start|>[read_file(path="log.txt", start=10, lines=5)]'
        "<|tool_call_end|>"
    )
    assert r.status is ParseStatus.CALL
    assert r.call.arguments == {"path": "log.txt", "start": 10, "lines": 5}


def test_lfm_pythonic_finish():
    a = get_adapter("lfm_pythonic")
    r = a.parse('<|tool_call_start|>[finish(answer="42")]<|tool_call_end|>')
    assert r.status is ParseStatus.CALL
    assert r.call.arguments == {"answer": "42"}


def test_lfm_pythonic_no_eval():
    """The parser must never evaluate arbitrary code."""
    a = get_adapter("lfm_pythonic")
    r = a.parse('<|tool_call_start|>[run(cmd=__import__("os").system("x"))]'
                "<|tool_call_end|>")
    assert r.status is ParseStatus.INVALID


def test_lfm_pythonic_positional():
    a = get_adapter("lfm_pythonic")
    r = a.parse('<|tool_call_start|>[run("ls")]<|tool_call_end|>')
    assert r.status is ParseStatus.CALL
    assert r.call.arguments == {"cmd": "ls"}


def test_hermes_valid():
    a = get_adapter("hermes")
    r = a.parse('<tool_call>{"name": "write_file", "arguments": '
                '{"path": "x.txt", "content": "hi"}}</tool_call>')
    assert r.status is ParseStatus.CALL
    assert r.call.name == "write_file"


def test_hermes_text_and_invalid():
    a = get_adapter("hermes")
    assert a.parse("no call").status is ParseStatus.TEXT
    assert a.parse("<tool_call>{oops</tool_call>").status is ParseStatus.INVALID


def test_openai_native_call():
    from tbnano.adapters.openai import OpenAIAdapter

    tc = [{"function": {"name": "run", "arguments": '{"cmd": "ls"}'}}]
    call = OpenAIAdapter.parse_native_call(tc)
    assert call.name == "run"
    assert call.arguments == {"cmd": "ls"}
    assert OpenAIAdapter.parse_native_call([]) is None


@pytest.mark.parametrize(
    "fmt", ["json_tags", "lfm_pythonic", "hermes", "openai"]
)
def test_system_prompt_budget(fmt):
    from tbnano.budgets import MAX_SYSTEM_TOKENS
    from tbnano.tokens import ApproxTokenizer

    a = get_adapter(fmt)
    n = ApproxTokenizer().count(a.system_prompt())
    assert n <= MAX_SYSTEM_TOKENS, f"{fmt} system prompt {n} tokens > budget"


def test_qwen_xml_parses_template_format():
    from tbnano.adapters import get_adapter
    ad = get_adapter("qwen_xml")
    r = ad.parse("<think>\nok\n</think>\n\n<tool_call>\n<function=read_file>\n<parameter=path>\na.txt\n</parameter>\n"
                 "<parameter=start>\n3\n</parameter>\n</function>\n</tool_call>")
    assert r.call.name == "read_file" and r.call.arguments == {"path": "a.txt", "start": 3}
    assert ad.parse("<tool_call>\n<function=nope>\n</function>\n</tool_call>").status.value == "invalid"
    assert ad.parse("just text").status.value == "text"
