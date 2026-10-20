import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '221,6,49\n446,1,76\n460,7,99\n480,4,44\n486,2,34\n537,8,81\n609,7,28\n630,7,11\n653,2,60\n715,1,11\n782,8,33\n833,3,49\n850,4,23\n879,8,77\n931,3,32\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
