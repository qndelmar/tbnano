import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '180,9,62\n206,8,51\n286,6,48\n321,8,79\n499,4,17\n547,1,67\n606,3,88\n696,3,20\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
