import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 2 payload\n[ERROR] event 10 payload\n[ERROR] event 12 payload\n[ERROR] event 37 payload\n[ERROR] event 41 payload\n[ERROR] event 42 payload\n'

def test_errors_file():
    p = BASE / "errors.txt"
    assert p.exists(), "errors.txt missing — did you run extract.sh?"
    assert p.read_text() == EXPECTED
