import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['128.238.32.87', '131.131.221.234', '17.29.40.183', '177.134.240.20', '202.33.62.172', '207.156.90.120', '209.146.163.153', '211.81.23.36', '44.159.174.106', '52.64.40.191', '58.15.112.214', '65.16.90.59', '75.181.12.244', '95.5.138.138', '96.244.38.77']

def test_ips_file():
    p = BASE / "clients.txt"
    assert p.exists(), "clients.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
