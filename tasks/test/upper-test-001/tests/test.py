import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'ALPHA56\nDELTA77\nBETA75\nECHO15\nGAMMA27\nECHO10\nECHO83\nALPHA9\nECHO26\nBETA15\nECHO47\nECHO38\nBETA50\n'
OUT = 'upper.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
