import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['109.18.24.137', '109.190.183.232', '115.122.114.212', '127.73.8.92', '153.74.31.206', '169.164.2.97', '175.186.78.93', '184.117.249.214', '19.182.61.138', '198.226.194.57', '219.41.156.49', '3.42.161.196', '63.1.34.141']

def test_ips_file():
    p = BASE / "clients.txt"
    assert p.exists(), "clients.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
