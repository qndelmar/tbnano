import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '14,a0\n94,a1\n93,a2\n64,a3\n33,a4\n93,a5\n50,a6\n57,a7\n39,a8\n70,a9\n17,a10\n57,a11\n75,a12\n'
OUT = 'rev.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
