import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['1.214.68.150', '104.214.64.84', '119.161.161.110', '124.104.120.45', '147.24.124.180', '186.245.43.148', '188.192.29.151', '200.242.224.68', '23.136.117.123', '234.72.123.231', '41.46.28.183', '86.208.183.191', '9.192.231.15', '95.225.240.104']

def test_ips_file():
    p = BASE / "clients.txt"
    assert p.exists(), "clients.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
