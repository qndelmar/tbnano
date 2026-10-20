import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '997\n985\n985\n738\n712\n563\n509\n476\n398\n398\n271\n236\n122\n108\n72\n67\n-49\n-168\n-180\n-186\n-227\n-345\n-352\n-368\n-454\n-465\n-497\n-524\n-591\n-602\n-658\n-675\n-726\n-732\n-733\n-822\n-864\n-971\n'
OUT = 'desc.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
