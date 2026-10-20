import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['125.152.252.240', '128.17.120.20', '141.188.134.188', '153.22.129.81', '165.177.21.186', '190.161.216.158', '202.11.130.23', '210.83.16.105', '213.11.24.16', '58.2.220.165', '73.15.101.47', '96.98.1.77']

def test_ips_file():
    p = BASE / "clients.txt"
    assert p.exists(), "clients.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
