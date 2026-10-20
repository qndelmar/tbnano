import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '126,u62,29\n163,u36,47\n192,u25,42\n449,u95,12\n550,u46,24\n639,u91,5\n812,u69,30\n865,u26,6\n891,u23,41\n963,u24,41\n'
OUT = 'joined.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
