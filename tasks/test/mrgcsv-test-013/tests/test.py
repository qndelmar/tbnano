import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '107,6,80\n125,1,11\n126,9,83\n364,6,12\n375,2,95\n401,9,87\n591,7,83\n717,7,15\n776,2,14\n780,5,48\n901,2,81\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
