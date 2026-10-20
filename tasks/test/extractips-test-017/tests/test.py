import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['133.140.147.98', '136.52.93.41', '137.244.13.219', '165.188.246.77', '200.128.85.29', '252.174.104.185', '57.100.117.146', '71.60.85.228']

def test_ips_file():
    p = BASE / "clients.txt"
    assert p.exists(), "clients.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
