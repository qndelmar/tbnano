import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '20,a0\n9,a1\n92,a2\n59,a3\n17,a4\n30,a5\n27,a6\n28,a7\n78,a8\n45,a9\n76,a10\n23,a11\n49,a12\n57,a13\n43,a14\n'
OUT = 'rev.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
