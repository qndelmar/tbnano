import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['114.82.53.194', '121.54.11.53', '133.19.53.23', '137.137.75.87', '154.134.130.137', '194.110.128.17', '242.24.138.3', '27.199.66.189', '79.252.3.112', '79.90.60.28']

def test_ips_file():
    p = BASE / "ips.txt"
    assert p.exists(), "ips.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
