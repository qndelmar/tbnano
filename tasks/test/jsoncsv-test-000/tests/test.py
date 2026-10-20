import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'id,v\n0,49\n1,69\n2,69\n3,91\n4,46\n5,96\n6,75\n7,95\n8,64\n9,92\n'
OUT = 'out.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
