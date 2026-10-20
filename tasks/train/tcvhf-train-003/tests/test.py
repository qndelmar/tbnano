import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '0,74\n1,70\n2,24\n3,75\n4,16\n5,9\n6,85\n7,15\n8,48\n9,71\n'
OUT = 'head.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
