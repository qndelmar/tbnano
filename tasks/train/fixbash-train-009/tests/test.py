import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 0 payload\n[ERROR] event 1 payload\n[ERROR] event 4 payload\n[ERROR] event 5 payload\n[ERROR] event 7 payload\n[ERROR] event 9 payload\n[ERROR] event 17 payload\n[ERROR] event 20 payload\n[ERROR] event 24 payload\n[ERROR] event 25 payload\n[ERROR] event 28 payload\n[ERROR] event 35 payload\n[ERROR] event 37 payload\n[ERROR] event 39 payload\n[ERROR] event 45 payload\n[ERROR] event 46 payload\n[ERROR] event 47 payload\n[ERROR] event 49 payload\n[ERROR] event 50 payload\n[ERROR] event 51 payload\n[ERROR] event 53 payload\n[ERROR] event 61 payload\n[ERROR] event 63 payload\n[ERROR] event 67 payload\n[ERROR] event 69 payload\n[ERROR] event 70 payload\n[ERROR] event 76 payload\n[ERROR] event 77 payload\n[ERROR] event 85 payload\n[ERROR] event 87 payload\n'

def test_errors_file():
    p = BASE / "hits.txt"
    assert p.exists(), "hits.txt missing — did you run filter.sh?"
    assert p.read_text() == EXPECTED
