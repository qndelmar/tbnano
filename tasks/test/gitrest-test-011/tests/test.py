import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_restored():
    p = BASE / "config.ini"
    assert p.exists(), "config.ini not restored"
    assert "payload-264" in p.read_text()
