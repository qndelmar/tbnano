import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '171,u95,43\n216,u10,10\n237,u20,30\n268,u27,22\n314,u62,36\n506,u98,29\n518,u19,8\n528,u36,6\n536,u67,49\n671,u47,33\n736,u19,1\n743,u82,1\n744,u52,44\n762,u11,11\n875,u43,48\n908,u16,46\n'
OUT = 'joined.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
