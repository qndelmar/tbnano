import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '122.117.119.180\n127.92.243.252\n146.96.32.180\n155.109.135.252\n168.76.19.104\n184.204.19.41\n195.15.225.78\n218.124.228.38\n225.189.194.232\n243.107.194.137\n247.251.189.176\n30.149.49.112\n35.64.2.86\n36.76.226.220\n67.226.121.17\n'
OUT = 'ips.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
