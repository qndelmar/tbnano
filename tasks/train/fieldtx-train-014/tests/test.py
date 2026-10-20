import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '783\n747\n195\n428\n453\n905\n791\n634\n772\n573\n437\n868\n612\n889\n781\n606\n105\n281\n919\n720\n133\n660\n185\n896\n398\n634\n248\n503\n809\n'

def test_output_file():
    p = BASE / "col.txt"
    assert p.exists(), "col.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
