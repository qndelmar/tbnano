import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "done.txt"
    assert p.exists(), "done.txt missing"
    assert "payload-7785" in p.read_text()
