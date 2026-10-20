import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_restored():
    p = BASE / "prefs.ini"
    assert p.exists(), "prefs.ini not restored"
    assert "hyperdrive-512" in p.read_text()
