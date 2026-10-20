import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 1 payload\n[ERROR] event 2 payload\n[ERROR] event 21 payload\n[ERROR] event 24 payload\n[ERROR] event 26 payload\n[ERROR] event 33 payload\n[ERROR] event 36 payload\n[ERROR] event 38 payload\n[ERROR] event 40 payload\n[ERROR] event 41 payload\n[ERROR] event 42 payload\n[ERROR] event 46 payload\n[ERROR] event 47 payload\n[ERROR] event 52 payload\n[ERROR] event 54 payload\n[ERROR] event 58 payload\n[ERROR] event 63 payload\n[ERROR] event 65 payload\n'

def test_errors_file():
    p = BASE / "found.txt"
    assert p.exists(), "found.txt missing — did you run scan.sh?"
    assert p.read_text() == EXPECTED
