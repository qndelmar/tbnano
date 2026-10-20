import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'r0\nr1\nr2\nr3\nr4\nr5\nr6\nr7\nr8\nr9\nr10\nr11\nr12\nr13\nr14\nr15\nr16\n'
OUT = 'extract.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
