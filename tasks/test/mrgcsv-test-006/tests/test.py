import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '117,9,46\n121,4,32\n125,8,73\n170,4,56\n174,8,16\n288,4,48\n330,4,13\n367,3,52\n370,6,55\n591,6,54\n711,5,54\n770,7,88\n775,3,15\n846,8,85\n881,3,14\n924,4,72\n950,7,83\n987,2,31\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
