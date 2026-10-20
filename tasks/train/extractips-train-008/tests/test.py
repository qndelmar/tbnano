import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['117.151.230.195', '123.63.101.55', '132.40.220.8', '199.153.132.237', '3.21.114.59', '36.99.105.159', '44.19.224.76', '59.229.180.134']

def test_ips_file():
    p = BASE / "addrs.txt"
    assert p.exists(), "addrs.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
