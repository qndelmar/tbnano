import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'dev25@corp.net\ndev78@a.com\nops69@a.com\nops6@corp.net\nqa74@a.com\nqa78@corp.net\nqa96@b.org\nroot54@corp.net\nroot81@corp.net\nsvc94@b.org\n'
OUT = 'emails.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
