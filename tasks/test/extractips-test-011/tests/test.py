import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = ['120.130.151.244', '15.202.189.66', '156.212.110.33', '182.29.200.125', '193.90.61.108', '199.120.68.170', '215.170.24.13', '34.201.223.240']

def test_ips_file():
    p = BASE / "ips.txt"
    assert p.exists(), "ips.txt missing"
    got = [l.strip() for l in p.read_text().splitlines() if l.strip()]
    assert got == EXPECTED, f"got {got}"
