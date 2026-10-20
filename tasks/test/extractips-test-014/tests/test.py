import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['100.39.146.150', '123.172.73.8', '138.144.147.133', '167.111.102.74', '169.174.227.124', '187.140.176.160', '199.48.60.253', '2.77.161.33', '245.119.145.77', '55.131.15.105', '6.32.113.28', '72.115.44.33', '72.247.220.58', '80.4.210.152', '99.248.116.248']

def test_ips_file():
    p = BASE / "clients.txt"
    assert p.exists(), "clients.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
