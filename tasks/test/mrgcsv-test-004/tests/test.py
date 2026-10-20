import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '131,2,22\n143,7,32\n199,7,42\n255,9,80\n257,7,58\n436,9,63\n450,7,40\n646,6,83\n711,8,67\n805,6,60\n817,6,13\n829,1,58\n835,6,28\n899,6,17\n913,6,24\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
