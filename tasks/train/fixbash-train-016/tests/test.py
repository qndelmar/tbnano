import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 1 payload\n[ERROR] event 9 payload\n[ERROR] event 12 payload\n[ERROR] event 18 payload\n[ERROR] event 19 payload\n[ERROR] event 20 payload\n[ERROR] event 22 payload\n[ERROR] event 25 payload\n[ERROR] event 29 payload\n[ERROR] event 35 payload\n[ERROR] event 36 payload\n[ERROR] event 50 payload\n[ERROR] event 51 payload\n[ERROR] event 54 payload\n[ERROR] event 62 payload\n[ERROR] event 66 payload\n[ERROR] event 67 payload\n'

def test_errors_file():
    p = BASE / "hits.txt"
    assert p.exists(), "hits.txt missing — did you run filter.sh?"
    assert p.read_text() == EXPECTED
