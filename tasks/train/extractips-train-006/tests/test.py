import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['119.251.126.178', '188.144.154.199', '194.116.77.203', '202.38.170.133', '253.222.134.85', '30.204.144.35']

def test_ips_file():
    p = BASE / "addrs.txt"
    assert p.exists(), "addrs.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
