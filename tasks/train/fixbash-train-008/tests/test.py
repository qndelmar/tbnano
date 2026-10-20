import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[ERROR] event 10 payload\n[ERROR] event 26 payload\n[ERROR] event 38 payload\n[ERROR] event 40 payload\n[ERROR] event 41 payload\n[ERROR] event 47 payload\n[ERROR] event 49 payload\n[ERROR] event 52 payload\n[ERROR] event 59 payload\n[ERROR] event 63 payload\n'

def test_errors_file():
    p = BASE / "hits.txt"
    assert p.exists(), "hits.txt missing — did you run scan.sh?"
    assert p.read_text() == EXPECTED
