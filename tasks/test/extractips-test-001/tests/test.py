import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['114.76.76.229', '119.78.40.191', '138.72.7.42', '150.151.27.19', '174.133.1.208', '194.148.95.107', '241.111.34.160', '5.138.98.131', '80.153.124.216', '88.189.215.46']

def test_ips_file():
    p = BASE / "clients.txt"
    assert p.exists(), "clients.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
