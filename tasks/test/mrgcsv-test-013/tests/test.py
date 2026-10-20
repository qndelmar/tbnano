import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '146,9,57\n155,3,98\n218,8,15\n229,8,22\n232,4,21\n271,6,30\n355,3,75\n364,8,64\n446,9,55\n732,1,16\n869,8,49\n937,5,83\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
