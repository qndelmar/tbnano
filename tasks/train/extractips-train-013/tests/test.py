import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['151.10.25.234', '158.107.51.225', '220.226.190.128', '52.68.127.53', '64.140.80.146', '65.49.23.209', '71.114.47.61', '99.179.9.166']

def test_ips_file():
    p = BASE / "sources.txt"
    assert p.exists(), "sources.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
