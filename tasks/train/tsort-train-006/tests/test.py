import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'elm29\nelm43\nelm54\nfig36\nfig44\nfig6\nfig91\nkiwi52\nkiwi54\nkiwi69\nkiwi71\nkiwi8\noak31\noak47\noak63\noak84\noak89\nplum39\nplum4\nplum50\nplum72\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
