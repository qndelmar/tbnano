import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'foxtrot fjord romeo delta whiskey\nuniform mike lima\nzulu xray xray echo\nfoxtrot jet golf cobalt\nuniform\n'
OUT = 'log.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
