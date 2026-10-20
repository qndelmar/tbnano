import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'w5\nw1\nw6\nw4\nw8\nw1\nw5\nw9\nw8\nw9\nw1\nw2\nw9\nw6\n'
OUT = 'extract.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
