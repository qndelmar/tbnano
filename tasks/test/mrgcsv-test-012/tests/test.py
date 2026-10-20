import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '189,3,54\n257,3,49\n310,1,20\n387,8,60\n391,6,98\n426,3,56\n471,9,75\n518,8,26\n550,1,74\n584,3,73\n597,4,31\n710,1,21\n715,8,41\n738,9,99\n791,1,59\n794,2,57\n849,2,23\n871,4,96\n934,7,50\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
