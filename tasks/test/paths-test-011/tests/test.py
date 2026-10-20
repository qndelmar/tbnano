import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "deployed/flag.txt"
    assert p.exists(), "deployed/flag.txt missing"
    assert "payload-6262" in p.read_text()
