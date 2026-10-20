import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '451\n9\n479\n354\n328\n368\n865\n792\n707\n363\n669\n881\n12\n718\n539\n918\n833\n818\n889\n933\n287\n185\n742\n10\n443\n985\n'

def test_output_file():
    p = BASE / "col.txt"
    assert p.exists(), "col.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
