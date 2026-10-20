import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'r22\nr21\nr20\nr19\nr18\nr17\nr16\nr15\nr14\nr13\nr12\nr11\nr10\nr9\nr8\nr7\nr6\nr5\nr4\nr3\nr2\nr1\nr0\n'
OUT = 'rev.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
