import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['10.57.75.16', '113.184.59.161', '130.93.234.124', '135.248.145.39', '173.131.24.137', '179.115.117.49', '186.29.118.116', '189.126.10.144', '196.106.79.96', '216.134.133.96', '224.151.180.107', '242.130.101.132', '51.89.253.166', '88.25.212.95', '90.48.128.233']

def test_ips_file():
    p = BASE / "ips.txt"
    assert p.exists(), "ips.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
