import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 0 payload\n[ERROR] event 4 payload\n[ERROR] event 9 payload\n[ERROR] event 12 payload\n[ERROR] event 21 payload\n[ERROR] event 28 payload\n[ERROR] event 38 payload\n[ERROR] event 39 payload\n[ERROR] event 42 payload\n[ERROR] event 49 payload\n[ERROR] event 64 payload\n[ERROR] event 66 payload\n[ERROR] event 74 payload\n[ERROR] event 82 payload\n[ERROR] event 84 payload\n[ERROR] event 86 payload\n[ERROR] event 88 payload\n[ERROR] event 90 payload\n[ERROR] event 102 payload\n[ERROR] event 104 payload\n[ERROR] event 107 payload\n[ERROR] event 110 payload\n[ERROR] event 113 payload\n'

def test_errors_file():
    p = BASE / "errors.txt"
    assert p.exists(), "errors.txt missing — did you run report.sh?"
    assert p.read_text() == EXPECTED
