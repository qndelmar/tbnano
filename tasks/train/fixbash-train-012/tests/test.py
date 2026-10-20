import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 1 payload\n[ERROR] event 3 payload\n[ERROR] event 5 payload\n[ERROR] event 6 payload\n[ERROR] event 9 payload\n[ERROR] event 11 payload\n[ERROR] event 13 payload\n[ERROR] event 14 payload\n[ERROR] event 15 payload\n[ERROR] event 16 payload\n[ERROR] event 19 payload\n[ERROR] event 20 payload\n[ERROR] event 21 payload\n[ERROR] event 22 payload\n[ERROR] event 25 payload\n[ERROR] event 27 payload\n[ERROR] event 31 payload\n[ERROR] event 32 payload\n[ERROR] event 34 payload\n[ERROR] event 35 payload\n[ERROR] event 36 payload\n[ERROR] event 38 payload\n[ERROR] event 39 payload\n[ERROR] event 40 payload\n'

def test_errors_file():
    p = BASE / "hits.txt"
    assert p.exists(), "hits.txt missing — did you run filter.sh?"
    assert p.read_text() == EXPECTED
