import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'ALPHA89\nGAMMA83\nBETA46\nGAMMA9\nECHO92\nECHO34\nECHO20\n'
OUT = 'upper.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
