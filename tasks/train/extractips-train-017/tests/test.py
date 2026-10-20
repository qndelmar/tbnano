import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['13.22.100.55', '146.54.38.184', '176.203.217.4', '210.207.120.196', '235.11.20.174', '242.4.184.82', '243.49.118.152', '81.20.229.214']

def test_ips_file():
    p = BASE / "addrs.txt"
    assert p.exists(), "addrs.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
