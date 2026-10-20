import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 6 payload\n[ERROR] event 10 payload\n[ERROR] event 22 payload\n[ERROR] event 39 payload\n[ERROR] event 44 payload\n[ERROR] event 46 payload\n[ERROR] event 49 payload\n[ERROR] event 53 payload\n[ERROR] event 56 payload\n[ERROR] event 70 payload\n[ERROR] event 91 payload\n[ERROR] event 92 payload\n[ERROR] event 104 payload\n[ERROR] event 111 payload\n'

def test_errors_file():
    p = BASE / "errors.txt"
    assert p.exists(), "errors.txt missing — did you run extract.sh?"
    assert p.read_text() == EXPECTED
