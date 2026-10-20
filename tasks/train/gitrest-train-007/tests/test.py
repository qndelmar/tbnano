import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_restored():
    p = BASE / "prefs.ini"
    assert p.exists(), "prefs.ini not restored"
    assert "booster-808" in p.read_text()
