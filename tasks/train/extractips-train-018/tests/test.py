import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['15.178.55.38', '153.150.113.247', '162.197.25.167', '195.101.80.223', '3.190.189.102', '42.160.40.47', '45.249.42.242', '84.243.17.240']

def test_ips_file():
    p = BASE / "addrs.txt"
    assert p.exists(), "addrs.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
