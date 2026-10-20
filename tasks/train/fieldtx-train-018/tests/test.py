import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '969\n566\n561\n521\n450\n386\n385\n384\n294\n36\n-334\n-388\n-579\n-603\n-621\n-633\n-756\n-820\n-926\n-974\n'

def test_output_file():
    p = BASE / "sorted.txt"
    assert p.exists(), "sorted.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
