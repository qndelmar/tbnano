import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 4 payload\n[ERROR] event 6 payload\n[ERROR] event 9 payload\n[ERROR] event 12 payload\n[ERROR] event 59 payload\n'

def test_errors_file():
    p = BASE / "found.txt"
    assert p.exists(), "found.txt missing — did you run scan.sh?"
    assert p.read_text() == EXPECTED
