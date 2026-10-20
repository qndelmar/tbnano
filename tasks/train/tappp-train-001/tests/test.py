import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'foxtrot papa\nember hotel mike uniform\ncobalt hotel sierra cobalt ion\nromeo xray uniform kilo november\nhotel\n'
OUT = 'log.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
