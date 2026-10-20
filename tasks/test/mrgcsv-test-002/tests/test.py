import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '312,5,92\n397,1,79\n407,4,60\n511,2,24\n737,9,12\n869,1,29\n888,6,50\n934,2,44\n941,4,59\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
