import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['102.179.158.183', '160.21.219.155', '183.110.61.135', '208.51.110.196', '23.1.50.248', '250.117.244.231', '29.223.50.48', '37.40.47.66', '54.84.71.76', '77.159.216.109', '84.169.3.220']

def test_ips_file():
    p = BASE / "addrs.txt"
    assert p.exists(), "addrs.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
