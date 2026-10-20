import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "staging/ok.txt"
    assert p.exists(), "staging/ok.txt missing"
    assert "payload-5251" in p.read_text()
