import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_dir_exists():
    assert (BASE / 'out75').is_dir(), "out75 missing"
