import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'DELTA79\nALPHA24\nALPHA64\nBETA97\nALPHA52\nECHO70\nBETA85\nDELTA72\nECHO34\nGAMMA9\nALPHA53\n'
OUT = 'upper.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
