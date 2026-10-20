import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['128.192.211.173', '132.140.212.88', '135.171.216.77', '138.161.250.76', '169.122.16.69', '177.192.112.242', '200.12.150.132', '212.11.214.166', '234.189.177.39', '235.76.189.59', '240.184.26.37', '69.159.50.68', '69.66.174.172', '85.13.143.195']

def test_ips_file():
    p = BASE / "ips.txt"
    assert p.exists(), "ips.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
