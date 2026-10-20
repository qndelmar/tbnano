import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'id,v\n0,69\n1,67\n2,9\n3,51\n4,29\n5,95\n6,76\n7,10\n8,55\n9,57\n10,32\n11,43\n12,39\n13,90\n14,65\n15,47\n16,70\n17,51\n'
OUT = 'out.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
