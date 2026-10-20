import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '/api/3\n/api/485\n/doc/245\n/doc/27\n/doc/354\n/doc/411\n/img/148\n/img/305\n/v2/289\n/v2/352\n/v2/394\n'
OUT = 'urls.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
