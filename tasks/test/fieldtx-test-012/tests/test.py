import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '689\n99\n717\n350\n710\n88\n192\n119\n156\n701\n322\n45\n550\n380\n454\n186\n327\n901\n104\n782\n959\n746\n894\n738\n238\n311\n234\n160\n507\n119\n460\n574\n712\n578\n294\n700\n694\n446\n846\n'

def test_output_file():
    p = BASE / "col.txt"
    assert p.exists(), "col.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
