import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['108.13.230.251', '125.155.239.1', '127.143.50.115', '139.142.61.98', '141.50.87.17', '161.126.82.224', '161.99.213.23', '164.110.183.137', '35.37.115.195', '38.252.54.167', '51.91.21.45', '88.45.68.122', '97.50.38.193']

def test_ips_file():
    p = BASE / "addrs.txt"
    assert p.exists(), "addrs.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
