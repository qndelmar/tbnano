import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '980\n938\n935\n765\n763\n675\n672\n661\n606\n532\n454\n368\n308\n235\n211\n171\n140\n122\n96\n-11\n-63\n-84\n-125\n-141\n-234\n-245\n-278\n-300\n-383\n-391\n-398\n-424\n-559\n-619\n-629\n-735\n-808\n-824\n-848\n-883\n-886\n-912\n'

def test_output_file():
    p = BASE / "sorted.txt"
    assert p.exists(), "sorted.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
