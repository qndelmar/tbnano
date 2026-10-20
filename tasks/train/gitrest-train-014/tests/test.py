import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_restored():
    p = BASE / "index.txt"
    assert p.exists(), "index.txt not restored"
    assert "payload-735" in p.read_text()
