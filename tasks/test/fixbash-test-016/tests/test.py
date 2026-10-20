import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 1 payload\n[ERROR] event 3 payload\n[ERROR] event 6 payload\n[ERROR] event 7 payload\n[ERROR] event 8 payload\n[ERROR] event 21 payload\n[ERROR] event 25 payload\n[ERROR] event 28 payload\n[ERROR] event 41 payload\n[ERROR] event 43 payload\n[ERROR] event 44 payload\n[ERROR] event 53 payload\n[ERROR] event 67 payload\n[ERROR] event 69 payload\n[ERROR] event 70 payload\n[ERROR] event 71 payload\n[ERROR] event 75 payload\n[ERROR] event 78 payload\n[ERROR] event 93 payload\n[ERROR] event 97 payload\n[ERROR] event 100 payload\n[ERROR] event 113 payload\n[ERROR] event 114 payload\n[ERROR] event 116 payload\n[ERROR] event 117 payload\n'

def test_errors_file():
    p = BASE / "errors.txt"
    assert p.exists(), "errors.txt missing — did you run report.sh?"
    assert p.read_text() == EXPECTED
