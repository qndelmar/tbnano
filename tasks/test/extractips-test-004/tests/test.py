import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '113.5.81.27\n160.142.59.39\n189.139.84.17\n189.146.187.3\n195.136.8.104\n8.173.75.176\n94.63.111.8\n'
OUT = 'clients.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
