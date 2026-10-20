import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 0 payload\n[ERROR] event 1 payload\n[ERROR] event 6 payload\n[ERROR] event 9 payload\n[ERROR] event 10 payload\n[ERROR] event 11 payload\n[ERROR] event 13 payload\n[ERROR] event 14 payload\n[ERROR] event 19 payload\n[ERROR] event 20 payload\n[ERROR] event 23 payload\n[ERROR] event 24 payload\n[ERROR] event 30 payload\n[ERROR] event 38 payload\n[ERROR] event 42 payload\n'

def test_errors_file():
    p = BASE / "errs.txt"
    assert p.exists(), "errs.txt missing — did you run extract.sh?"
    assert p.read_text() == EXPECTED
