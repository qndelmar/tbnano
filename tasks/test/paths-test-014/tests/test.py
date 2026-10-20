import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_output():
    p = BASE / "out_dir/marker.txt"
    assert p.exists(), "out_dir/marker.txt missing"
    assert "payload-3743" in p.read_text()
