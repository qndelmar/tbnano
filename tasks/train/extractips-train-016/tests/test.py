import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['122.246.116.27', '182.232.105.116', '201.216.93.134', '29.63.142.217', '34.52.7.15', '43.228.81.67', '60.118.243.158']

def test_ips_file():
    p = BASE / "sources.txt"
    assert p.exists(), "sources.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
