import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 0 payload\n[ERROR] event 5 payload\n[ERROR] event 6 payload\n[ERROR] event 9 payload\n[ERROR] event 12 payload\n[ERROR] event 13 payload\n[ERROR] event 14 payload\n[ERROR] event 17 payload\n[ERROR] event 24 payload\n[ERROR] event 26 payload\n[ERROR] event 29 payload\n[ERROR] event 30 payload\n[ERROR] event 33 payload\n[ERROR] event 42 payload\n[ERROR] event 48 payload\n'

def test_errors_file():
    p = BASE / "found.txt"
    assert p.exists(), "found.txt missing — did you run filter.sh?"
    assert p.read_text() == EXPECTED
