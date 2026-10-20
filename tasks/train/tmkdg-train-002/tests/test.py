import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_dir_exists():
    assert (BASE / 'results66').is_dir(), "results66 missing"
