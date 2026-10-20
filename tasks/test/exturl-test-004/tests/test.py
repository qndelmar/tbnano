import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '/api/156\n/api/38\n/doc/204\n/doc/36\n/doc/388\n/doc/395\n/doc/77\n/img/116\n/img/194\n/img/272\n/v2/450\n/v2/81\n'
OUT = 'urls.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
