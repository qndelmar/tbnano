import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '215,3,67\n273,1,58\n282,5,78\n289,6,25\n293,3,25\n316,6,26\n330,8,14\n363,5,78\n377,3,16\n382,1,45\n406,2,19\n439,6,93\n480,9,96\n813,9,96\n901,9,87\n945,4,56\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
