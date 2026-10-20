import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['127.239.214.211', '13.90.150.241', '143.30.223.52', '154.80.47.210', '160.167.211.166', '178.107.28.222', '21.3.168.205', '217.2.245.124', '250.200.55.2', '250.253.214.58', '35.214.136.47', '70.5.231.130', '83.183.12.149', '88.164.221.222']

def test_ips_file():
    p = BASE / "sources.txt"
    assert p.exists(), "sources.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
