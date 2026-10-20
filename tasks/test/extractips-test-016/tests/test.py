import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['101.17.149.140', '102.191.23.137', '111.42.219.62', '117.82.215.150', '158.4.117.245', '186.1.250.131', '193.39.84.135', '222.7.22.23', '23.57.22.142', '93.179.180.94']

def test_ips_file():
    p = BASE / "ips.txt"
    assert p.exists(), "ips.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
