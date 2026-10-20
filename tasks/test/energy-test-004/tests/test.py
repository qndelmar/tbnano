import os, math, re
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
ANSWER_FILE = BASE / ".submission" / "answer.txt"
EXPECTED = 409.19047763888886
REL_TOL = 0.001

def _read_answer():
    env = os.environ.get("TBNANO_ANSWER")
    if env is not None:
        return env
    if ANSWER_FILE.exists():
        return ANSWER_FILE.read_text().strip()
    return ""

def _parse_number(s):
    m = re.findall(r"-?\d+\.?\d*(?:[eE][-+]?\d+)?", s)
    return float(m[-1]) if m else None

def test_answer_present():
    assert _read_answer() != "", "no answer submitted"

def test_answer_value():
    got = _parse_number(_read_answer())
    assert got is not None, f"could not parse a number from answer"
    exp = float(EXPECTED)
    assert math.isclose(got, exp, rel_tol=REL_TOL), f"got {got}, expected {exp}"
