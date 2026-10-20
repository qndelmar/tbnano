import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'elm1\nelm82\nelm83\nelm86\nelm94\nelm98\nfig1\nfig14\nfig24\nfig61\nkiwi76\nkiwi94\nkiwi97\noak21\noak22\noak47\noak57\noak80\noak89\nplum36\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
