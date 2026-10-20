import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_restored():
    p = BASE / "crew.txt"
    assert p.exists(), "crew.txt not restored"
    assert "hyperdrive-156" in p.read_text()
