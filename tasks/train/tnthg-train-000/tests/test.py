import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
ANSWER_FILE = BASE / ".submission" / "answer.txt"
EXPECTED = 'whiskey echo sierra ember tango'

def _read_answer():
    env = os.environ.get("TBNANO_ANSWER")
    if env is not None:
        return env
    if ANSWER_FILE.exists():
        return ANSWER_FILE.read_text()
    return ""

def test_answer_present():
    assert _read_answer().strip() != "", "no answer submitted"

def test_answer_value():
    got = " ".join(_read_answer().split()).strip().lower()
    exp = " ".join(EXPECTED.split()).strip().lower()
    assert got == exp, f"got {got!r}, expected {exp!r}"
