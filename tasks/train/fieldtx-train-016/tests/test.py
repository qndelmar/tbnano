import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '968\n966\n919\n902\n895\n891\n818\n732\n654\n637\n577\n562\n548\n542\n458\n353\n229\n207\n177\n147\n102\n26\n-6\n-27\n-39\n-99\n-149\n-177\n-189\n-238\n-260\n-271\n-347\n-446\n-506\n-528\n-582\n-724\n-776\n-791\n-804\n-813\n-867\n'

def test_output_file():
    p = BASE / "sorted.txt"
    assert p.exists(), "sorted.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
