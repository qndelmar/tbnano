import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "drop/done.txt"
    assert p.exists(), "drop/done.txt missing"
    assert "payload-6486" in p.read_text()
