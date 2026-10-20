import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'id,v\n0,65\n1,34\n2,83\n3,16\n4,83\n5,60\n6,82\n7,32\n8,25\n9,22\n10,48\n11,57\n12,95\n13,93\n14,75\n15,21\n16,21\n17,78\n18,32\n19,98\n20,14\n'
OUT = 'out.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
