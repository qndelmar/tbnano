import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 12 payload\n[ERROR] event 34 payload\n[ERROR] event 36 payload\n[ERROR] event 41 payload\n[ERROR] event 98 payload\n[ERROR] event 105 payload\n'

def test_errors_file():
    p = BASE / "errs.txt"
    assert p.exists(), "errs.txt missing — did you run report.sh?"
    assert p.read_text() == EXPECTED
