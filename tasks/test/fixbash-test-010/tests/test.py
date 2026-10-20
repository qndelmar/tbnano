import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 0 payload\n[ERROR] event 2 payload\n[ERROR] event 4 payload\n[ERROR] event 6 payload\n[ERROR] event 7 payload\n[ERROR] event 10 payload\n[ERROR] event 11 payload\n[ERROR] event 12 payload\n[ERROR] event 13 payload\n[ERROR] event 16 payload\n[ERROR] event 17 payload\n[ERROR] event 21 payload\n[ERROR] event 25 payload\n[ERROR] event 26 payload\n[ERROR] event 27 payload\n[ERROR] event 29 payload\n[ERROR] event 32 payload\n[ERROR] event 35 payload\n[ERROR] event 37 payload\n[ERROR] event 39 payload\n[ERROR] event 41 payload\n[ERROR] event 42 payload\n[ERROR] event 43 payload\n[ERROR] event 47 payload\n[ERROR] event 49 payload\n[ERROR] event 51 payload\n[ERROR] event 54 payload\n[ERROR] event 58 payload\n[ERROR] event 59 payload\n[ERROR] event 63 payload\n'

def test_errors_file():
    p = BASE / "errors.txt"
    assert p.exists(), "errors.txt missing — did you run report.sh?"
    assert p.read_text() == EXPECTED
