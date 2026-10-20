import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '188,9,97\n262,5,49\n270,7,69\n298,2,61\n351,4,79\n423,7,53\n427,3,38\n509,5,87\n660,3,11\n735,3,27\n854,8,76\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
