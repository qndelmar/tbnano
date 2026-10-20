import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 0 payload\n[ERROR] event 4 payload\n[ERROR] event 8 payload\n[ERROR] event 14 payload\n[ERROR] event 17 payload\n[ERROR] event 41 payload\n[ERROR] event 51 payload\n[ERROR] event 52 payload\n[ERROR] event 56 payload\n[ERROR] event 59 payload\n[ERROR] event 62 payload\n[ERROR] event 64 payload\n[ERROR] event 65 payload\n[ERROR] event 83 payload\n[ERROR] event 85 payload\n[ERROR] event 88 payload\n[ERROR] event 105 payload\n[ERROR] event 108 payload\n'

def test_errors_file():
    p = BASE / "hits.txt"
    assert p.exists(), "hits.txt missing — did you run filter.sh?"
    assert p.read_text() == EXPECTED
