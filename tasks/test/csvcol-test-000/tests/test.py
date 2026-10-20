import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'w3\nw5\nw5\nw6\nw8\nw7\nw3\nw5\nw7\nw7\nw9\nw8\nw2\nw4\nw6\nw3\nw3\nw6\nw1\n'
OUT = 'extract.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
