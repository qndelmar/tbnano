import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '13,a0\n38,a1\n40,a2\n48,a3\n50,a4\n25,a5\n96,a6\n97,a7\n86,a8\n75,a9\n44,a10\n52,a11\n35,a12\n7,a13\n97,a14\n'
OUT = 'rev.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
