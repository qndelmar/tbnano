import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '107.101.28.21\n133.109.8.118\n204.150.210.167\n216.37.120.207\n228.134.12.9\n237.103.178.141\n242.248.196.13\n85.21.89.154\n'
OUT = 'clients.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
