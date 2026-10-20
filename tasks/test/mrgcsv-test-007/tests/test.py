import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '105,5,80\n158,1,47\n168,9,86\n199,4,30\n227,6,69\n285,5,50\n308,5,70\n415,2,41\n712,6,38\n762,1,56\n814,3,41\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
