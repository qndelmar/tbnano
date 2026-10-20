import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['1.191.125.193', '118.176.57.143', '120.75.103.3', '124.60.204.122', '132.54.28.90', '145.7.50.101', '156.8.87.144', '160.44.170.97', '221.48.196.81', '29.56.69.179', '39.41.104.195', '96.151.111.111']

def test_ips_file():
    p = BASE / "addrs.txt"
    assert p.exists(), "addrs.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
