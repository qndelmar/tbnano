import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'delta echo kilo november\nmike xray whiskey echo alpha\noscar whiskey juliet ember sierra\nsierra yankee zulu echo bravo\nquebec\n'
OUT = 'log.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
