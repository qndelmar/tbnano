import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 2 payload\n[ERROR] event 5 payload\n[ERROR] event 7 payload\n[ERROR] event 11 payload\n[ERROR] event 12 payload\n[ERROR] event 14 payload\n[ERROR] event 19 payload\n[ERROR] event 21 payload\n[ERROR] event 27 payload\n[ERROR] event 29 payload\n[ERROR] event 31 payload\n[ERROR] event 32 payload\n[ERROR] event 37 payload\n[ERROR] event 39 payload\n[ERROR] event 40 payload\n[ERROR] event 48 payload\n[ERROR] event 49 payload\n[ERROR] event 50 payload\n[ERROR] event 52 payload\n[ERROR] event 53 payload\n[ERROR] event 56 payload\n[ERROR] event 59 payload\n[ERROR] event 67 payload\n[ERROR] event 75 payload\n[ERROR] event 83 payload\n[ERROR] event 88 payload\n'

def test_errors_file():
    p = BASE / "found.txt"
    assert p.exists(), "found.txt missing — did you run filter.sh?"
    assert p.read_text() == EXPECTED
