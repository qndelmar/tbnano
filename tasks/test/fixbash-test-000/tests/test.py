import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 31 payload\n[ERROR] event 35 payload\n[ERROR] event 45 payload\n'

def test_errors_file():
    p = BASE / "errors.txt"
    assert p.exists(), "errors.txt missing — did you run report.sh?"
    assert p.read_text() == EXPECTED
