import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['122.207.2.113', '158.119.114.38', '158.195.83.154', '19.202.248.111', '207.90.29.190', '247.13.200.159', '35.223.14.213', '49.82.228.179']

def test_ips_file():
    p = BASE / "addrs.txt"
    assert p.exists(), "addrs.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
