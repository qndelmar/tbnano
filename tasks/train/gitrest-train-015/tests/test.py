import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_restored():
    p = BASE / "diary.txt"
    assert p.exists(), "diary.txt not restored"
    assert "payload-431" in p.read_text()
