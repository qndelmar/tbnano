import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 0 payload\n[ERROR] event 6 payload\n[ERROR] event 10 payload\n[ERROR] event 14 payload\n[ERROR] event 19 payload\n[ERROR] event 40 payload\n[ERROR] event 43 payload\n[ERROR] event 46 payload\n[ERROR] event 48 payload\n[ERROR] event 68 payload\n[ERROR] event 70 payload\n'

def test_errors_file():
    p = BASE / "errs.txt"
    assert p.exists(), "errs.txt missing — did you run report.sh?"
    assert p.read_text() == EXPECTED
