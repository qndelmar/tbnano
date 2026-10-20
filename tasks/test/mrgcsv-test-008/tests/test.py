import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '118,2,65\n162,6,78\n261,3,55\n271,8,75\n294,6,72\n330,2,84\n350,3,65\n439,6,34\n456,2,80\n736,6,34\n764,1,57\n815,1,95\n822,6,40\n838,3,28\n854,1,89\n878,9,39\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
