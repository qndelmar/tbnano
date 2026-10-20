import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 6 payload\n[ERROR] event 37 payload\n[ERROR] event 46 payload\n[ERROR] event 57 payload\n[ERROR] event 60 payload\n[ERROR] event 100 payload\n[ERROR] event 102 payload\n'

def test_errors_file():
    p = BASE / "hits.txt"
    assert p.exists(), "hits.txt missing — did you run scan.sh?"
    assert p.read_text() == EXPECTED
