import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['117.111.58.142', '143.114.168.231', '16.176.205.228', '164.76.210.146', '186.39.26.196', '199.34.206.141', '203.45.127.91', '206.39.104.221', '212.193.36.38', '224.63.76.102', '230.106.179.27', '32.215.172.217', '56.184.233.106', '90.2.234.152']

def test_ips_file():
    p = BASE / "clients.txt"
    assert p.exists(), "clients.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
