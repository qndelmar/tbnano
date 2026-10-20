import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "flag.txt"
    assert p.exists(), "flag.txt missing"
    assert "payload-1065" in p.read_text()
