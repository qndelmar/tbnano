import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'ECHO29\nALPHA37\nALPHA77\nALPHA40\nECHO99\nBETA7\nECHO73\nGAMMA54\nECHO68\nALPHA42\nDELTA76\nALPHA17\nGAMMA44\nBETA3\n'
OUT = 'upper.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
