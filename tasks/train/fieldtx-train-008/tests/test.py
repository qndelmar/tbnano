import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '767\n740\n999\n766\n838\n820\n563\n372\n962\n742\n796\n503\n342\n36\n248\n579\n676\n832\n366\n926\n499\n607\n675\n259\n142\n137\n409\n'

def test_output_file():
    p = BASE / "col.txt"
    assert p.exists(), "col.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
