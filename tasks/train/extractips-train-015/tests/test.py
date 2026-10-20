import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['1.116.168.252', '113.14.131.166', '151.140.182.37', '195.235.138.93', '196.80.111.60', '213.207.22.234', '214.118.112.180', '219.232.196.72', '226.168.222.162', '23.92.208.215', '236.242.170.184', '4.248.36.160', '50.198.194.193']

def test_ips_file():
    p = BASE / "addrs.txt"
    assert p.exists(), "addrs.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
