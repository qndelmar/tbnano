import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '974\n805\n597\n560\n486\n430\n308\n290\n191\n187\n70\n24\n-26\n-31\n-128\n-143\n-358\n-482\n-591\n-629\n-732\n-771\n-781\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
