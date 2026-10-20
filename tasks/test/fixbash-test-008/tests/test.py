import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 0 payload\n[ERROR] event 5 payload\n[ERROR] event 7 payload\n[ERROR] event 8 payload\n[ERROR] event 14 payload\n[ERROR] event 17 payload\n[ERROR] event 25 payload\n[ERROR] event 29 payload\n[ERROR] event 30 payload\n[ERROR] event 31 payload\n[ERROR] event 36 payload\n[ERROR] event 44 payload\n[ERROR] event 46 payload\n[ERROR] event 49 payload\n[ERROR] event 50 payload\n[ERROR] event 53 payload\n[ERROR] event 57 payload\n[ERROR] event 60 payload\n[ERROR] event 72 payload\n[ERROR] event 73 payload\n[ERROR] event 76 payload\n[ERROR] event 77 payload\n[ERROR] event 79 payload\n[ERROR] event 83 payload\n[ERROR] event 84 payload\n[ERROR] event 86 payload\n[ERROR] event 87 payload\n[ERROR] event 88 payload\n'

def test_errors_file():
    p = BASE / "errs.txt"
    assert p.exists(), "errs.txt missing — did you run report.sh?"
    assert p.read_text() == EXPECTED
