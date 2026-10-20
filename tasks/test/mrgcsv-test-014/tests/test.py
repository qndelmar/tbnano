import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '152,3,46\n413,4,62\n416,3,18\n422,5,64\n424,9,81\n459,4,99\n488,5,12\n504,7,93\n519,5,86\n732,5,98\n735,4,29\n789,8,65\n832,1,13\n877,8,71\n886,6,39\n888,8,54\n933,6,35\n937,7,74\n961,5,77\n994,7,20\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
