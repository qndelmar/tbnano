import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 1 payload\n[ERROR] event 10 payload\n[ERROR] event 19 payload\n[ERROR] event 25 payload\n[ERROR] event 30 payload\n[ERROR] event 39 payload\n[ERROR] event 47 payload\n[ERROR] event 49 payload\n[ERROR] event 54 payload\n[ERROR] event 59 payload\n[ERROR] event 62 payload\n[ERROR] event 71 payload\n[ERROR] event 79 payload\n[ERROR] event 80 payload\n'

def test_errors_file():
    p = BASE / "found.txt"
    assert p.exists(), "found.txt missing — did you run scan.sh?"
    assert p.read_text() == EXPECTED
