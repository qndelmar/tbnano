import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '120,6,12\n121,3,65\n130,3,54\n178,6,16\n316,8,32\n323,3,38\n337,1,99\n401,5,98\n427,5,46\n524,9,21\n584,8,64\n678,7,68\n679,6,86\n694,8,34\n787,7,66\n897,5,40\n931,1,24\n941,9,31\n981,9,77\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
