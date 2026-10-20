import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "out.txt"
    assert p.exists(), "out.txt missing"
    assert "payload-7516" in p.read_text()
