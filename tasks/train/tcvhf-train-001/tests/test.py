import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '0,96\n1,38\n2,37\n3,41\n4,33\n5,38\n6,65\n7,1\n8,51\n'
OUT = 'head.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
