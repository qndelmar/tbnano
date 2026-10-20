import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'elm14\nelm2\nelm49\nkiwi25\nkiwi30\nkiwi60\nkiwi73\noak53\noak83\nplum25\nplum26\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
