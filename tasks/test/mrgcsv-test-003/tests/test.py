import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '209,7,94\n214,7,79\n233,6,10\n285,4,73\n304,2,75\n358,7,73\n420,3,51\n584,9,85\n586,7,23\n611,7,80\n695,1,50\n753,4,89\n814,5,91\n842,3,33\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
