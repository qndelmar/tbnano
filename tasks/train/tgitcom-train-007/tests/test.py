import os, subprocess
from pathlib import Path
BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_file_present():
    assert (BASE / "f.txt").exists()

def test_committed():
    assert (BASE / "f.txt").read_text() == "v1\nv2\n"
    log = subprocess.run(["git", "-C", str(BASE), "log", "--format=%s"],
                         capture_output=True, text=True).stdout
    assert "upd" in log
