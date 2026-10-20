import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['113.70.207.154', '134.193.4.204', '177.99.122.188', '193.139.176.76', '193.149.167.253', '227.120.219.218', '23.198.17.16', '249.175.193.183', '4.11.40.222', '49.146.177.60', '50.229.3.208', '63.63.156.112', '89.211.206.163', '89.9.137.223', '94.42.202.162']

def test_ips_file():
    p = BASE / "clients.txt"
    assert p.exists(), "clients.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
