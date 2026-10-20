import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'dev17@a.com\ndev37@corp.net\ndev3@a.com\ndev81@b.org\nops67@a.com\nqa34@b.org\nqa34@corp.net\nsvc54@b.org\nsvc65@a.com\n'
OUT = 'emails.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
