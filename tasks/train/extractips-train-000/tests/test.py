import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['105.47.156.60', '159.239.117.107', '204.173.44.216', '236.51.125.128', '250.76.184.228', '31.100.98.211', '45.100.47.18', '92.238.198.33', '93.195.179.202']

def test_ips_file():
    p = BASE / "addrs.txt"
    assert p.exists(), "addrs.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
