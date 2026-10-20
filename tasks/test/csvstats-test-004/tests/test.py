import math, os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = {'min': 11.0, 'max': 498.0, 'sum': 11229.0}

def test_file_present():
    assert (BASE / 'stats.txt').exists(), "stats.txt missing"

def test_kv():
    kv = {}
    for line in (BASE / 'stats.txt').read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            kv[k.strip()] = float(v)
    for k, v in EXPECTED.items():
        assert k in kv, f"{k} missing"
        assert math.isclose(kv[k], v, rel_tol=1e-09), f"{k}: {kv[k]} != {v}"
