import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '143.11.95.112\n148.204.46.241\n157.140.54.183\n163.100.111.58\n77.247.213.131\n95.124.220.99\n98.113.127.104\n'
OUT = 'clients.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
