import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'v0,k0\nv1,k1\nv2,k2\nv3,k3\nv4,k4\nv5,k5\nv6,k6\nv7,k7\nv8,k8\nv9,k9\nv10,k10\nv11,k11\nv12,k12\nv13,k13\nv14,k14\n'
OUT = 'swapped.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
