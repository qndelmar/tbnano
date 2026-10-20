import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '/api/116\n/api/215\n/api/228\n/api/232\n/api/350\n/api/73\n/doc/210\n/doc/365\n/doc/494\n/v2/415\n/v2/71\n/v2/75\n'
OUT = 'urls.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
