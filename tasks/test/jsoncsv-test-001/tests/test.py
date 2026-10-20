import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'id,v\n0,19\n1,52\n2,57\n3,56\n4,69\n5,90\n6,50\n7,25\n8,71\n9,10\n10,21\n11,61\n12,43\n13,80\n14,75\n'
OUT = 'out.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
