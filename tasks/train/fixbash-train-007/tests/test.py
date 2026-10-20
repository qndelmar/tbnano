import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 1 payload\n[ERROR] event 6 payload\n[ERROR] event 8 payload\n[ERROR] event 9 payload\n[ERROR] event 14 payload\n[ERROR] event 17 payload\n[ERROR] event 18 payload\n[ERROR] event 20 payload\n[ERROR] event 21 payload\n[ERROR] event 22 payload\n[ERROR] event 29 payload\n[ERROR] event 31 payload\n[ERROR] event 32 payload\n[ERROR] event 35 payload\n[ERROR] event 38 payload\n[ERROR] event 41 payload\n[ERROR] event 42 payload\n[ERROR] event 45 payload\n[ERROR] event 54 payload\n[ERROR] event 57 payload\n[ERROR] event 61 payload\n[ERROR] event 65 payload\n[ERROR] event 69 payload\n[ERROR] event 70 payload\n[ERROR] event 71 payload\n[ERROR] event 73 payload\n[ERROR] event 75 payload\n[ERROR] event 77 payload\n[ERROR] event 80 payload\n[ERROR] event 81 payload\n'

def test_errors_file():
    p = BASE / "found.txt"
    assert p.exists(), "found.txt missing — did you run filter.sh?"
    assert p.read_text() == EXPECTED
