import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "deployed/marker.txt"
    assert p.exists(), "deployed/marker.txt missing"
    assert "payload-5783" in p.read_text()
