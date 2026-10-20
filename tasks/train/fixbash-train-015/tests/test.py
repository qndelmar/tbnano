import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 3 payload\n[ERROR] event 8 payload\n[ERROR] event 9 payload\n[ERROR] event 13 payload\n[ERROR] event 16 payload\n[ERROR] event 20 payload\n[ERROR] event 22 payload\n[ERROR] event 26 payload\n[ERROR] event 36 payload\n[ERROR] event 39 payload\n[ERROR] event 42 payload\n[ERROR] event 47 payload\n[ERROR] event 51 payload\n[ERROR] event 61 payload\n[ERROR] event 66 payload\n[ERROR] event 69 payload\n'

def test_errors_file():
    p = BASE / "found.txt"
    assert p.exists(), "found.txt missing — did you run filter.sh?"
    assert p.read_text() == EXPECTED
