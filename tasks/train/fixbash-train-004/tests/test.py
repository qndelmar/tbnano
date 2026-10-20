import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 2 payload\n[ERROR] event 37 payload\n[ERROR] event 39 payload\n[ERROR] event 40 payload\n[ERROR] event 52 payload\n[ERROR] event 56 payload\n'

def test_errors_file():
    p = BASE / "found.txt"
    assert p.exists(), "found.txt missing — did you run filter.sh?"
    assert p.read_text() == EXPECTED
