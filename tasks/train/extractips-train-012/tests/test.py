import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['105.180.144.220', '147.69.93.141', '151.238.182.229', '153.56.84.210', '162.115.62.48', '177.63.8.163', '179.63.18.103', '203.142.120.218', '212.90.167.29', '219.204.93.11', '22.211.218.89', '223.238.166.119', '240.55.32.126', '52.36.19.89', '99.87.89.150']

def test_ips_file():
    p = BASE / "sources.txt"
    assert p.exists(), "sources.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
