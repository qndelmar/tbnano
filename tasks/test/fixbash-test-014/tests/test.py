import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 8 payload\n[ERROR] event 12 payload\n[ERROR] event 17 payload\n[ERROR] event 23 payload\n[ERROR] event 26 payload\n[ERROR] event 32 payload\n[ERROR] event 36 payload\n[ERROR] event 39 payload\n[ERROR] event 40 payload\n[ERROR] event 44 payload\n[ERROR] event 53 payload\n[ERROR] event 54 payload\n[ERROR] event 57 payload\n[ERROR] event 62 payload\n[ERROR] event 66 payload\n[ERROR] event 70 payload\n'

def test_errors_file():
    p = BASE / "errors.txt"
    assert p.exists(), "errors.txt missing — did you run extract.sh?"
    assert p.read_text() == EXPECTED
