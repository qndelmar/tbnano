import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '31\n469\n232\n342\n613\n200\n45\n176\n604\n144\n430\n578\n114\n543\n202\n390\n574\n252\n50\n903\n305\n943\n829\n467\n761\n263\n243\n242\n340\n78\n'

def test_output_file():
    p = BASE / "col.txt"
    assert p.exists(), "col.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
