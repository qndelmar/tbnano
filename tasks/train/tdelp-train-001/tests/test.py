import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_gone():
    assert not (BASE / "junk.tmp").exists(), "junk.tmp still exists"
