import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '138.211.205.244\n14.245.137.233\n159.117.21.236\n162.123.84.170\n164.134.237.58\n164.239.1.20\n190.102.80.196\n203.142.55.89\n204.227.214.24\n249.169.6.117\n3.2.87.187\n45.101.195.134\n9.132.88.24\n9.43.117.131\n'
OUT = 'clients.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
