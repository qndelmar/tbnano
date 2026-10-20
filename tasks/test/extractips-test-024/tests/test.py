import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['11.76.62.86', '128.14.40.254', '151.180.155.252', '154.159.17.48', '161.78.211.136', '17.170.54.101', '197.140.40.2', '198.124.226.167', '41.53.10.14', '78.83.17.245', '85.71.146.113', '9.146.225.141']

def test_ips_file():
    p = BASE / "clients.txt"
    assert p.exists(), "clients.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
