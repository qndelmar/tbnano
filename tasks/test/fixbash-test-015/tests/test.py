import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 2 payload\n[ERROR] event 3 payload\n[ERROR] event 6 payload\n[ERROR] event 9 payload\n[ERROR] event 13 payload\n[ERROR] event 14 payload\n[ERROR] event 15 payload\n[ERROR] event 18 payload\n[ERROR] event 20 payload\n[ERROR] event 23 payload\n[ERROR] event 26 payload\n[ERROR] event 29 payload\n[ERROR] event 33 payload\n[ERROR] event 34 payload\n[ERROR] event 41 payload\n[ERROR] event 42 payload\n[ERROR] event 43 payload\n[ERROR] event 44 payload\n[ERROR] event 49 payload\n[ERROR] event 52 payload\n[ERROR] event 55 payload\n[ERROR] event 56 payload\n[ERROR] event 60 payload\n[ERROR] event 61 payload\n[ERROR] event 63 payload\n[ERROR] event 68 payload\n'

def test_errors_file():
    p = BASE / "errs.txt"
    assert p.exists(), "errs.txt missing — did you run extract.sh?"
    assert p.read_text() == EXPECTED
