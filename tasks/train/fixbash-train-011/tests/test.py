import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 2 payload\n[ERROR] event 9 payload\n[ERROR] event 20 payload\n[ERROR] event 22 payload\n[ERROR] event 39 payload\n[ERROR] event 40 payload\n[ERROR] event 68 payload\n[ERROR] event 78 payload\n[ERROR] event 79 payload\n[ERROR] event 81 payload\n[ERROR] event 84 payload\n'

def test_errors_file():
    p = BASE / "found.txt"
    assert p.exists(), "found.txt missing — did you run filter.sh?"
    assert p.read_text() == EXPECTED
