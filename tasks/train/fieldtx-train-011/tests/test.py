import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '745\n530\n621\n462\n940\n944\n522\n720\n594\n625\n602\n258\n375\n622\n801\n598\n630\n638\n345\n381\n491\n801\n145\n312\n889\n465\n67\n153\n427\n'

def test_output_file():
    p = BASE / "col.txt"
    assert p.exists(), "col.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
