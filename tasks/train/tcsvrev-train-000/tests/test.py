import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '95,a0\n42,a1\n45,a2\n59,a3\n20,a4\n55,a5\n91,a6\n38,a7\n'
OUT = 'rev.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
