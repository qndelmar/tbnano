import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_restored():
    p = BASE / "notes.txt"
    assert p.exists(), "notes.txt not restored"
    assert "hyperdrive-969" in p.read_text()
