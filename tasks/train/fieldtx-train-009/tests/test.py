import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '994\n907\n896\n863\n789\n785\n656\n621\n615\n565\n434\n428\n385\n345\n313\n298\n284\n256\n218\n208\n164\n144\n124\n112\n102\n2\n-5\n-137\n-153\n-189\n-348\n-495\n-526\n-542\n-616\n-651\n-689\n-743\n-744\n-785\n-895\n-910\n-913\n-917\n'

def test_output_file():
    p = BASE / "sorted.txt"
    assert p.exists(), "sorted.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
