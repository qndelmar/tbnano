import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['116.178.157.182', '118.12.231.226', '118.208.203.193', '121.220.191.91', '123.32.73.245', '138.127.57.205', '140.178.80.149', '15.187.210.58', '151.57.121.57', '168.144.228.75', '253.179.173.175', '7.123.188.51', '75.135.89.74', '82.183.65.50']

def test_ips_file():
    p = BASE / "ips.txt"
    assert p.exists(), "ips.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
