import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '278,9,93\n300,7,16\n302,9,38\n454,9,37\n554,7,68\n585,2,61\n653,6,90\n697,9,31\n699,7,77\n751,9,26\n826,1,96\n855,1,21\n869,8,24\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
