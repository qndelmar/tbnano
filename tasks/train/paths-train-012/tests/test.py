import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "res.txt"
    assert p.exists(), "res.txt missing"
    assert "payload-3154" in p.read_text()
