import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_restored():
    p = BASE / "manifest.txt"
    assert p.exists(), "manifest.txt not restored"
    assert "telemetry-951" in p.read_text()
