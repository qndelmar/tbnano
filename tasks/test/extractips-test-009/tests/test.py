import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['114.158.139.113', '128.242.58.208', '155.39.117.170', '175.150.82.156', '175.203.195.91', '190.248.107.22', '228.242.83.138', '234.208.127.238', '24.194.50.218', '252.81.32.27', '86.238.145.72', '93.58.93.148', '94.140.243.50']

def test_ips_file():
    p = BASE / "ips.txt"
    assert p.exists(), "ips.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
