import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'GAMMA81\nDELTA8\nALPHA21\nBETA37\nGAMMA49\nDELTA87\nGAMMA40\nDELTA78\nALPHA92\nGAMMA60\nGAMMA47\nBETA53\nALPHA95\n'
OUT = 'upper.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
