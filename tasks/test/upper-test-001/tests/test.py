import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'GAMMA31\nDELTA19\nGAMMA42\nALPHA1\nBETA91\nECHO67\nECHO60\nGAMMA23\nBETA87\nGAMMA16\n'
OUT = 'upper.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
