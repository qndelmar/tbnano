import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 3 payload\n[ERROR] event 12 payload\n[ERROR] event 13 payload\n[ERROR] event 23 payload\n[ERROR] event 46 payload\n[ERROR] event 51 payload\n[ERROR] event 54 payload\n[ERROR] event 62 payload\n[ERROR] event 63 payload\n[ERROR] event 66 payload\n[ERROR] event 67 payload\n[ERROR] event 83 payload\n'

def test_errors_file():
    p = BASE / "found.txt"
    assert p.exists(), "found.txt missing — did you run scan.sh?"
    assert p.read_text() == EXPECTED
