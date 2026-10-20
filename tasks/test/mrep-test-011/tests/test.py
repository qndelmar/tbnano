import math, os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = {'apogee_m': 1200.0, 't_apogee_s': 8.0, 'vmax_ms': 60.0}

def test_file_present():
    assert (BASE / 'report.txt').exists(), "report.txt missing"

def test_kv():
    kv = {}
    for line in (BASE / 'report.txt').read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            kv[k.strip()] = float(v)
    for k, v in EXPECTED.items():
        assert k in kv, f"{k} missing"
        assert math.isclose(kv[k], v, rel_tol=0.0001), f"{k}: {kv[k]} != {v}"
