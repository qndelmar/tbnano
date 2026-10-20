import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 2 payload\n[ERROR] event 4 payload\n[ERROR] event 5 payload\n[ERROR] event 10 payload\n[ERROR] event 12 payload\n[ERROR] event 15 payload\n[ERROR] event 18 payload\n[ERROR] event 21 payload\n[ERROR] event 27 payload\n[ERROR] event 30 payload\n[ERROR] event 35 payload\n[ERROR] event 36 payload\n[ERROR] event 38 payload\n[ERROR] event 39 payload\n[ERROR] event 42 payload\n[ERROR] event 43 payload\n[ERROR] event 44 payload\n[ERROR] event 45 payload\n[ERROR] event 48 payload\n[ERROR] event 49 payload\n[ERROR] event 50 payload\n[ERROR] event 52 payload\n[ERROR] event 56 payload\n[ERROR] event 59 payload\n[ERROR] event 63 payload\n[ERROR] event 64 payload\n[ERROR] event 67 payload\n'

def test_errors_file():
    p = BASE / "errs.txt"
    assert p.exists(), "errs.txt missing — did you run extract.sh?"
    assert p.read_text() == EXPECTED
