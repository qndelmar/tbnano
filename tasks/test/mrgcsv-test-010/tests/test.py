import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '123,2,12\n126,4,91\n158,8,83\n159,2,38\n175,8,43\n199,6,71\n378,8,54\n517,9,78\n518,8,65\n599,8,74\n605,3,54\n606,6,14\n651,6,89\n709,7,11\n803,2,73\n859,6,69\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
