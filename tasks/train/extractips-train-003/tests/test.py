import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['146.38.114.220', '152.159.1.185', '193.233.150.70', '238.141.182.198', '42.182.57.26', '5.91.59.175', '72.157.236.72', '8.241.97.132']

def test_ips_file():
    p = BASE / "addrs.txt"
    assert p.exists(), "addrs.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
