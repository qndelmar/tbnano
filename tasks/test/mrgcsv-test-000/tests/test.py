import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '157,8,95\n188,1,48\n207,1,31\n683,2,37\n734,8,48\n850,4,51\n852,4,14\n869,7,63\n961,7,18\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
