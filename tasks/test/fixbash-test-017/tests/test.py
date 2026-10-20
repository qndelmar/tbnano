import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 7 payload\n[ERROR] event 50 payload\n[ERROR] event 63 payload\n[ERROR] event 70 payload\n[ERROR] event 71 payload\n[ERROR] event 76 payload\n'

def test_errors_file():
    p = BASE / "errors.txt"
    assert p.exists(), "errors.txt missing — did you run extract.sh?"
    assert p.read_text() == EXPECTED
