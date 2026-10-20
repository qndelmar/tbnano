import math, os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_report():
    p = BASE / "summary.txt"
    assert p.exists(), "summary.txt missing"
    kv = {}
    for line in p.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            kv[k.strip()] = float(v)
    assert math.isclose(kv["duration_s"], 9967, rel_tol=1e-9)
    assert math.isclose(kv["max_alt_m"], 9175.82112, rel_tol=1e-6)
    assert math.isclose(kv["fuel_kg"], 151.908084713, rel_tol=1e-6)
