import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['134.100.135.87', '170.16.242.50', '210.111.236.107', '46.219.111.146', '52.217.125.227', '90.140.78.40']

def test_ips_file():
    p = BASE / "ips.txt"
    assert p.exists(), "ips.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
