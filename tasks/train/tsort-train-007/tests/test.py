import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'elm3\nelm59\nelm6\nelm62\nelm9\nfig28\nfig48\nfig98\nkiwi35\nkiwi61\nkiwi86\nkiwi89\noak54\noak84\nplum32\nplum59\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
