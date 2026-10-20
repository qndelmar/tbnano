import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'elm51\nelm76\nelm81\nfig15\nfig34\nfig54\nfig89\nkiwi3\nkiwi37\nkiwi59\noak26\noak3\noak67\noak76\noak86\nplum2\nplum47\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
