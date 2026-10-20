import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['109.144.85.249', '128.14.126.16', '171.191.68.215', '239.223.44.62', '74.150.62.114', '81.166.141.43']

def test_ips_file():
    p = BASE / "sources.txt"
    assert p.exists(), "sources.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
