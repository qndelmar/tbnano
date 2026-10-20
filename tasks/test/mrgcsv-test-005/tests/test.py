import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '153,6,70\n219,7,85\n240,1,32\n315,2,72\n380,1,43\n419,2,23\n428,1,66\n497,3,21\n505,9,69\n580,5,81\n584,6,56\n594,5,31\n640,3,84\n815,1,70\n903,8,66\n920,1,51\n923,6,23\n972,4,46\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
