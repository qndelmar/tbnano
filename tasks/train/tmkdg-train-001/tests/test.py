import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_dir_exists():
    assert (BASE / 'build24').is_dir(), "build24 missing"
