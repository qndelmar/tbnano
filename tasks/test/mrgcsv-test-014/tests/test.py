import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '178,5,63\n190,7,94\n212,3,25\n412,8,30\n416,9,86\n549,4,96\n553,8,87\n680,6,54\n860,6,32\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
