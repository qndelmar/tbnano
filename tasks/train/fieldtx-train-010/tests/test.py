import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '844\n807\n780\n761\n719\n689\n670\n622\n531\n491\n273\n272\n247\n238\n163\n136\n4\n-45\n-46\n-113\n-127\n-193\n-201\n-312\n-348\n-351\n-414\n-420\n-440\n-445\n-476\n-646\n-727\n-809\n-829\n-858\n-860\n-957\n-998\n'

def test_output_file():
    p = BASE / "sorted.txt"
    assert p.exists(), "sorted.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
