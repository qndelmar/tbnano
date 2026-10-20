import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 5 payload\n[ERROR] event 36 payload\n[ERROR] event 38 payload\n[ERROR] event 48 payload\n[ERROR] event 54 payload\n[ERROR] event 57 payload\n[ERROR] event 69 payload\n[ERROR] event 77 payload\n[ERROR] event 87 payload\n[ERROR] event 93 payload\n[ERROR] event 96 payload\n[ERROR] event 97 payload\n[ERROR] event 98 payload\n[ERROR] event 99 payload\n[ERROR] event 109 payload\n'

def test_errors_file():
    p = BASE / "found.txt"
    assert p.exists(), "found.txt missing — did you run scan.sh?"
    assert p.read_text() == EXPECTED
