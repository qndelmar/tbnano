import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['106.214.113.82', '109.179.173.105', '119.249.76.246', '12.233.239.191', '121.214.235.199', '141.116.172.76', '197.14.206.239', '242.232.67.36', '26.101.232.15', '48.161.171.24', '62.108.142.246', '85.233.29.172']

def test_ips_file():
    p = BASE / "ips.txt"
    assert p.exists(), "ips.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
