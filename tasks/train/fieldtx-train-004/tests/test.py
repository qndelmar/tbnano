import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '706\n579\n570\n862\n71\n972\n909\n408\n943\n129\n188\n970\n157\n302\n769\n511\n761\n624\n726\n642\n192\n346\n313\n799\n822\n108\n602\n515\n390\n417\n'

def test_output_file():
    p = BASE / "col.txt"
    assert p.exists(), "col.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
