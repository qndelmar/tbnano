import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '107,5,33\n136,4,36\n146,2,96\n198,1,75\n212,3,28\n281,9,58\n321,6,49\n349,6,21\n372,1,18\n377,6,56\n480,4,88\n570,3,82\n766,8,64\n855,5,48\n870,1,87\n995,4,56\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
