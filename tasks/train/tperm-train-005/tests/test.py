import os
from pathlib import Path
BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_file_present():
    assert (BASE / "out.txt").exists()

def test_content():
    assert (BASE / "out.txt").read_text() == (BASE / "secret.txt").read_text()
