import math, os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))

def test_thrust():
    p = BASE / "thrust_n.txt"
    assert p.exists(), "thrust_n.txt missing — run thrust.py"
    got = float(p.read_text().strip())
    assert math.isclose(got, -9658.358184, rel_tol=1e-6), f"{got} != -9658.358184"
