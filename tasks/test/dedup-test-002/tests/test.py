import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'w103\nw513\nw709\nw984\nw929\nw437\nw859\nw729\nw531\nw561\nw942\nw705\n'
OUT = 'dedup.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
