import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '89,a0\n50,a1\n25,a2\n53,a3\n34,a4\n60,a5\n90,a6\n82,a7\n5,a8\n36,a9\n86,a10\n43,a11\n28,a12\n70,a13\n59,a14\n55,a15\n6,a16\n'
OUT = 'rev.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
