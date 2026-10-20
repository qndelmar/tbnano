import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '103,4,58\n118,3,77\n180,1,86\n198,5,32\n211,7,58\n274,8,77\n422,9,81\n448,6,15\n536,3,20\n548,5,35\n602,9,32\n627,5,42\n648,2,84\n665,9,44\n808,9,40\n855,3,10\n856,1,29\n860,9,28\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
