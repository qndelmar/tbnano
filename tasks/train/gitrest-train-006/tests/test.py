import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_restored():
    p = BASE / "team.txt"
    assert p.exists(), "team.txt not restored"
    assert "gyro-670" in p.read_text()
