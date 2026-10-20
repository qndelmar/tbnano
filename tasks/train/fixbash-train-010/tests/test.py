import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 2 payload\n[ERROR] event 4 payload\n[ERROR] event 7 payload\n[ERROR] event 12 payload\n[ERROR] event 16 payload\n[ERROR] event 19 payload\n[ERROR] event 20 payload\n[ERROR] event 21 payload\n[ERROR] event 26 payload\n[ERROR] event 27 payload\n[ERROR] event 36 payload\n[ERROR] event 64 payload\n[ERROR] event 66 payload\n[ERROR] event 67 payload\n[ERROR] event 72 payload\n[ERROR] event 73 payload\n[ERROR] event 74 payload\n[ERROR] event 76 payload\n[ERROR] event 78 payload\n[ERROR] event 83 payload\n[ERROR] event 85 payload\n[ERROR] event 88 payload\n[ERROR] event 90 payload\n[ERROR] event 93 payload\n[ERROR] event 100 payload\n[ERROR] event 102 payload\n[ERROR] event 103 payload\n[ERROR] event 104 payload\n[ERROR] event 106 payload\n'

def test_errors_file():
    p = BASE / "hits.txt"
    assert p.exists(), "hits.txt missing — did you run scan.sh?"
    assert p.read_text() == EXPECTED
