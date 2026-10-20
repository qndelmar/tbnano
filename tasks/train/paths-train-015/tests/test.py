import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "end.txt"
    assert p.exists(), "end.txt missing"
    assert "payload-2907" in p.read_text()
