import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'GAMMA90\nGAMMA61\nECHO25\nBETA86\nGAMMA99\nGAMMA31\nBETA42\nDELTA48\nECHO4\nDELTA73\nGAMMA89\nBETA70\nGAMMA17\nGAMMA90\nBETA37\nGAMMA37\nECHO1\nALPHA25\n'
OUT = 'upper.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
