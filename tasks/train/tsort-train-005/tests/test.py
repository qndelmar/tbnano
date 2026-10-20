import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'elm11\nelm97\nelm99\nfig85\nkiwi1\nkiwi22\nkiwi4\nkiwi59\nkiwi65\nkiwi8\nkiwi84\noak16\noak32\noak34\nplum99\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
