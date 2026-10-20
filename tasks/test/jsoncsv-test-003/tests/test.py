import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'id,v\n0,84\n1,1\n2,59\n3,89\n4,41\n5,97\n6,97\n7,18\n8,89\n9,22\n10,11\n11,18\n12,32\n13,27\n14,24\n15,10\n16,71\n17,64\n18,94\n19,55\n20,64\n21,24\n22,44\n23,43\n24,57\n25,47\n26,20\n27,75\n28,31\n'
OUT = 'out.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
