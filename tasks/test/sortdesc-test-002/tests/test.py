import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '942\n831\n781\n597\n575\n568\n560\n458\n454\n262\n152\n146\n116\n98\n43\n12\n-159\n-445\n-449\n-531\n-560\n-704\n-729\n-760\n-936\n'
OUT = 'desc.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
