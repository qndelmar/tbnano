import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['100.135.102.111', '144.45.55.27', '15.33.84.194', '181.116.14.214', '2.84.120.40', '204.95.236.247', '29.191.12.110', '9.53.61.106', '93.180.88.141']

def test_ips_file():
    p = BASE / "clients.txt"
    assert p.exists(), "clients.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
