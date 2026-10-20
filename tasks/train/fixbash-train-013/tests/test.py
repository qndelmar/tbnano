import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 0 payload\n[ERROR] event 4 payload\n[ERROR] event 6 payload\n[ERROR] event 9 payload\n[ERROR] event 23 payload\n[ERROR] event 24 payload\n[ERROR] event 25 payload\n[ERROR] event 26 payload\n[ERROR] event 32 payload\n[ERROR] event 35 payload\n[ERROR] event 38 payload\n[ERROR] event 43 payload\n[ERROR] event 47 payload\n[ERROR] event 48 payload\n[ERROR] event 53 payload\n[ERROR] event 59 payload\n[ERROR] event 62 payload\n[ERROR] event 65 payload\n'

def test_errors_file():
    p = BASE / "hits.txt"
    assert p.exists(), "hits.txt missing — did you run filter.sh?"
    assert p.read_text() == EXPECTED
