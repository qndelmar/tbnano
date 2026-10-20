import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '45,a0\n55,a1\n24,a2\n90,a3\n99,a4\n19,a5\n1,a6\n26,a7\n28,a8\n59,a9\n59,a10\n75,a11\n93,a12\n82,a13\n57,a14\n'
OUT = 'rev.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
