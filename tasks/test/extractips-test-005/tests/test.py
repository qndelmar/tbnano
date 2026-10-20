import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['123.202.194.236', '14.31.12.169', '140.115.183.62', '182.137.135.38', '213.45.111.205', '224.34.141.78', '248.72.94.227', '27.253.228.64', '54.200.19.251', '59.87.89.71', '70.155.101.162', '86.126.70.141', '9.101.124.119', '97.234.115.15']

def test_ips_file():
    p = BASE / "ips.txt"
    assert p.exists(), "ips.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
