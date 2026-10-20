import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '328,6,27\n348,6,63\n372,5,44\n438,5,83\n513,6,31\n647,5,78\n738,3,67\n739,4,87\n825,9,85\n884,6,45\n909,9,47\n981,9,25\n983,2,39\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
