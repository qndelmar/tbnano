import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'ECHO29\nGAMMA33\nBETA4\nGAMMA99\nBETA17\nGAMMA18\nALPHA81\nECHO73\n'
OUT = 'upper.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
