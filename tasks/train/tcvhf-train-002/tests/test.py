import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '0,36\n1,31\n2,13\n3,60\n4,74\n5,92\n6,78\n7,30\n8,25\n'
OUT = 'head.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
