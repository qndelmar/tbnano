import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 8 payload\n[ERROR] event 9 payload\n[ERROR] event 11 payload\n[ERROR] event 13 payload\n[ERROR] event 16 payload\n[ERROR] event 23 payload\n[ERROR] event 27 payload\n[ERROR] event 30 payload\n[ERROR] event 33 payload\n[ERROR] event 39 payload\n[ERROR] event 49 payload\n[ERROR] event 50 payload\n[ERROR] event 51 payload\n[ERROR] event 59 payload\n[ERROR] event 61 payload\n[ERROR] event 65 payload\n[ERROR] event 67 payload\n[ERROR] event 68 payload\n[ERROR] event 72 payload\n[ERROR] event 75 payload\n[ERROR] event 84 payload\n[ERROR] event 93 payload\n[ERROR] event 95 payload\n[ERROR] event 100 payload\n[ERROR] event 111 payload\n[ERROR] event 115 payload\n'

def test_errors_file():
    p = BASE / "errors.txt"
    assert p.exists(), "errors.txt missing — did you run report.sh?"
    assert p.read_text() == EXPECTED
