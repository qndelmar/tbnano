import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '997\n855\n820\n803\n761\n659\n521\n232\n187\n95\n61\n59\n-36\n-50\n-66\n-68\n-91\n-280\n-371\n-509\n-636\n-772\n-897\n-931\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
