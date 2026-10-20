import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '649\n257\n482\n965\n637\n183\n625\n528\n984\n272\n700\n836\n401\n533\n899\n713\n726\n60\n561\n384\n731\n999\n91\n186\n289\n443\n585\n217\n471\n831\n64\n233\n901\n435\n54\n94\n68\n889\n387\n713\n'

def test_output_file():
    p = BASE / "col.txt"
    assert p.exists(), "col.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
