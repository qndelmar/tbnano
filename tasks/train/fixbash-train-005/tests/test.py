import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 5 payload\n[ERROR] event 6 payload\n[ERROR] event 9 payload\n[ERROR] event 10 payload\n[ERROR] event 16 payload\n[ERROR] event 17 payload\n[ERROR] event 29 payload\n[ERROR] event 48 payload\n[ERROR] event 53 payload\n[ERROR] event 57 payload\n[ERROR] event 61 payload\n[ERROR] event 67 payload\n[ERROR] event 77 payload\n[ERROR] event 79 payload\n[ERROR] event 83 payload\n[ERROR] event 105 payload\n[ERROR] event 118 payload\n'

def test_errors_file():
    p = BASE / "hits.txt"
    assert p.exists(), "hits.txt missing — did you run filter.sh?"
    assert p.read_text() == EXPECTED
