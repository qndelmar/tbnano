import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['10.9.183.249', '120.68.203.115', '143.69.20.20', '166.138.251.242', '166.34.243.147', '173.171.236.132', '203.91.1.1', '230.120.76.197', '65.194.82.143', '70.201.135.27', '75.65.61.72']

def test_ips_file():
    p = BASE / "addrs.txt"
    assert p.exists(), "addrs.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
