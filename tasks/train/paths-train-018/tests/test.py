import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "staging/done.txt"
    assert p.exists(), "staging/done.txt missing"
    assert "payload-5671" in p.read_text()
