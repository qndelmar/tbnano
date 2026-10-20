import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 21 payload\n[ERROR] event 37 payload\n[ERROR] event 40 payload\n[ERROR] event 44 payload\n[ERROR] event 48 payload\n'

def test_errors_file():
    p = BASE / "errs.txt"
    assert p.exists(), "errs.txt missing — did you run report.sh?"
    assert p.read_text() == EXPECTED
