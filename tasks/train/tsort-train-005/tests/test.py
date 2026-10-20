import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'elm91\nfig34\nfig37\nfig49\nfig73\nfig87\nfig92\nkiwi16\nkiwi31\nkiwi39\nkiwi72\nkiwi83\nkiwi84\noak32\noak58\noak77\noak77\nplum35\nplum5\nplum54\nplum69\nplum82\nplum83\nplum92\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
