import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '134,9,81\n151,1,68\n213,6,19\n281,4,27\n345,8,23\n414,9,30\n554,8,85\n566,6,70\n574,4,39\n629,8,45\n630,6,16\n647,2,31\n860,9,23\n929,7,97\n980,8,58\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
