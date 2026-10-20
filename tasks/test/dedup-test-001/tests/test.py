import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'w187\nw755\nw432\nw631\nw627\nw969\nw172\nw287\nw712\nw624\nw527\n'
OUT = 'dedup.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
