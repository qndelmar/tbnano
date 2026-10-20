import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '155,9,99\n166,8,35\n562,1,36\n694,2,14\n715,4,76\n757,3,96\n842,3,37\n846,9,19\n926,5,88\n948,3,60\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
