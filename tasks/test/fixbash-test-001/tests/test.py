import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 4 payload\n[ERROR] event 15 payload\n[ERROR] event 18 payload\n[ERROR] event 25 payload\n[ERROR] event 32 payload\n[ERROR] event 36 payload\n[ERROR] event 37 payload\n[ERROR] event 43 payload\n[ERROR] event 46 payload\n[ERROR] event 48 payload\n[ERROR] event 55 payload\n[ERROR] event 58 payload\n[ERROR] event 63 payload\n[ERROR] event 71 payload\n[ERROR] event 73 payload\n[ERROR] event 75 payload\n[ERROR] event 81 payload\n[ERROR] event 86 payload\n[ERROR] event 92 payload\n'

def test_errors_file():
    p = BASE / "errs.txt"
    assert p.exists(), "errs.txt missing — did you run extract.sh?"
    assert p.read_text() == EXPECTED
