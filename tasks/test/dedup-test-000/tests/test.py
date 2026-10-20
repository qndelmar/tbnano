import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'w606\nw170\nw243\nw178\nw822\nw421\nw379\nw760\nw729\nw382\nw596\nw914\n'
OUT = 'dedup.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
