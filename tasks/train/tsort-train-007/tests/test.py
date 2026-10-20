import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'elm2\nelm20\nelm29\nelm50\nelm74\nelm76\nfig56\nfig59\nfig7\nkiwi19\nkiwi23\noak45\noak55\noak79\noak80\noak86\nplum3\nplum30\nplum37\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
