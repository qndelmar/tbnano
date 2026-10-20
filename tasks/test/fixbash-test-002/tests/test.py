import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 0 payload\n[ERROR] event 2 payload\n[ERROR] event 11 payload\n[ERROR] event 24 payload\n[ERROR] event 27 payload\n[ERROR] event 37 payload\n[ERROR] event 43 payload\n[ERROR] event 47 payload\n[ERROR] event 51 payload\n[ERROR] event 53 payload\n[ERROR] event 62 payload\n[ERROR] event 72 payload\n'

def test_errors_file():
    p = BASE / "errors.txt"
    assert p.exists(), "errors.txt missing — did you run report.sh?"
    assert p.read_text() == EXPECTED
