import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '788\n955\n787\n535\n684\n636\n67\n156\n908\n743\n10\n526\n916\n99\n657\n277\n295\n14\n954\n176\n639\n52\n833\n439\n'

def test_output_file():
    p = BASE / "col.txt"
    assert p.exists(), "col.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
