import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['115.51.103.119', '123.177.1.183', '128.165.159.212', '217.24.127.205', '220.110.239.17', '24.213.151.80', '248.184.179.188', '5.243.20.20', '64.198.8.112', '78.153.44.195', '78.41.59.226', '98.153.149.167']

def test_ips_file():
    p = BASE / "addrs.txt"
    assert p.exists(), "addrs.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
