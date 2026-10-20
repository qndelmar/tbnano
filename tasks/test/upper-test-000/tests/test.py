import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'BETA9\nALPHA21\nDELTA14\nALPHA78\nBETA1\nALPHA77\nGAMMA90\nBETA24\nBETA56\nALPHA85\n'
OUT = 'upper.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
