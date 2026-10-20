import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '23\n153\n620\n173\n263\n168\n927\n187\n731\n884\n853\n4\n192\n407\n213\n377\n360\n801\n104\n343\n387\n59\n266\n695\n914\n586\n576\n152\n650\n603\n70\n816\n508\n926\n136\n319\n'

def test_output_file():
    p = BASE / "col.txt"
    assert p.exists(), "col.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
