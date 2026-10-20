import os
from pathlib import Path
BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_file_present():
    assert (BASE / "keep.txt").exists()

def test_cleaned():
    assert not list(BASE.glob("*.tmp")), "tmp files remain"
