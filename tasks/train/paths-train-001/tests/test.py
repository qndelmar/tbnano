import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "drop/ok.txt"
    assert p.exists(), "drop/ok.txt missing"
    assert "payload-1945" in p.read_text()
