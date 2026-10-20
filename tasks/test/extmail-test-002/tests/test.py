import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'dev4@corp.net\nops41@a.com\nops67@a.com\nops94@a.com\nroot30@corp.net\nroot72@b.org\nsvc32@b.org\n'
OUT = 'senders.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
