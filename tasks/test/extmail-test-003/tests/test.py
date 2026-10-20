import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'dev5@b.org\ndev66@corp.net\ndev96@corp.net\nroot40@a.com\nroot7@a.com\nsvc26@b.org\nsvc31@b.org\nsvc36@a.com\nsvc57@b.org\n'
OUT = 'emails.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
