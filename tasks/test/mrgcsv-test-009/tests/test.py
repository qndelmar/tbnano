import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '233,5,72\n320,6,71\n409,8,43\n436,7,65\n460,8,50\n532,8,47\n642,2,32\n643,6,24\n768,1,34\n795,1,75\n833,2,13\n986,4,79\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
