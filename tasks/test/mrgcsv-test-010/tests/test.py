import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '158,2,55\n251,6,20\n317,9,42\n318,5,19\n347,9,76\n376,8,68\n396,5,24\n457,3,28\n466,6,48\n506,8,79\n567,9,14\n757,9,31\n767,4,91\n837,3,57\n869,4,62\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
