import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '129,2,21\n134,3,58\n147,4,21\n180,4,47\n201,2,74\n244,8,12\n513,3,40\n574,6,72\n671,9,95\n767,4,80\n987,1,83\n998,6,96\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
