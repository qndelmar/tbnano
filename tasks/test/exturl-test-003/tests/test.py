import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '/api/255\n/doc/178\n/doc/368\n/doc/376\n/doc/392\n/img/214\n/img/233\n/img/292\n/img/317\n/img/428\n/img/498\n/v2/194\n/v2/2\n/v2/458\n'
OUT = 'urls.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
