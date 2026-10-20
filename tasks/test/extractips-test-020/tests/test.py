import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['103.59.145.117', '111.104.49.166', '131.126.113.9', '157.252.76.229', '165.129.36.249', '248.165.205.237', '35.117.153.181']

def test_ips_file():
    p = BASE / "ips.txt"
    assert p.exists(), "ips.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
