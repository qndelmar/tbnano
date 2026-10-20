import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 20 payload\n[ERROR] event 67 payload\n[ERROR] event 99 payload\n[ERROR] event 103 payload\n[ERROR] event 107 payload\n'

def test_errors_file():
    p = BASE / "errors.txt"
    assert p.exists(), "errors.txt missing — did you run extract.sh?"
    assert p.read_text() == EXPECTED
