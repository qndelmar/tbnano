import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "result.txt"
    assert p.exists(), "result.txt missing"
    assert "payload-5736" in p.read_text()
