import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '158,2,85\n238,3,11\n268,2,17\n277,9,50\n310,6,34\n330,2,92\n489,5,23\n537,1,38\n560,9,99\n567,7,89\n583,5,29\n664,8,39\n668,7,71\n673,5,98\n787,2,23\n886,1,94\n995,7,27\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
