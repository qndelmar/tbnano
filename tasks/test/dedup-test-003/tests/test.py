import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'w895\nw742\nw155\nw344\nw829\nw847\nw967\nw723\nw294\nw467\nw809\nw544\n'
OUT = 'dedup.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
