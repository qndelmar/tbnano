import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 0 payload\n[ERROR] event 1 payload\n[ERROR] event 4 payload\n[ERROR] event 8 payload\n[ERROR] event 9 payload\n[ERROR] event 11 payload\n[ERROR] event 13 payload\n[ERROR] event 21 payload\n[ERROR] event 25 payload\n[ERROR] event 26 payload\n[ERROR] event 28 payload\n[ERROR] event 30 payload\n[ERROR] event 33 payload\n[ERROR] event 34 payload\n[ERROR] event 35 payload\n[ERROR] event 39 payload\n[ERROR] event 44 payload\n[ERROR] event 47 payload\n[ERROR] event 51 payload\n[ERROR] event 52 payload\n[ERROR] event 53 payload\n[ERROR] event 55 payload\n[ERROR] event 56 payload\n[ERROR] event 57 payload\n[ERROR] event 60 payload\n[ERROR] event 61 payload\n[ERROR] event 64 payload\n[ERROR] event 70 payload\n[ERROR] event 72 payload\n[ERROR] event 75 payload\n'

def test_errors_file():
    p = BASE / "errors.txt"
    assert p.exists(), "errors.txt missing — did you run report.sh?"
    assert p.read_text() == EXPECTED
