import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'id,v\n0,2\n1,64\n2,67\n3,17\n4,53\n5,68\n6,67\n7,18\n8,71\n9,44\n10,34\n11,92\n12,72\n13,19\n14,81\n15,8\n16,80\n17,54\n18,65\n19,79\n20,6\n21,33\n'
OUT = 'out.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
