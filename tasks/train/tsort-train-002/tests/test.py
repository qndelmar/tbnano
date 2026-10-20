import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'elm2\nfig30\nfig47\nfig85\nfig88\nkiwi14\nkiwi34\nkiwi85\noak43\noak54\noak54\noak71\nplum45\nplum66\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
