import os, subprocess
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_file_present():
    assert (BASE / "count.sh").exists(), "count.sh missing"

def test_out():
    assert (BASE / "out.txt").exists(), "out.txt missing"
    exp = subprocess.run(["grep", "-c", "^fail$", str(BASE / "results.txt")],
                         capture_output=True, text=True).stdout
    assert (BASE / "out.txt").read_text() == exp
