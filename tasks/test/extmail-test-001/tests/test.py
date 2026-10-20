import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'dev72@b.org\nops10@corp.net\nops25@a.com\nops50@a.com\nqa42@corp.net\nqa82@corp.net\nroot44@corp.net\nroot82@corp.net\nsvc37@a.com\nsvc5@b.org\nsvc90@a.com\n'
OUT = 'emails.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
