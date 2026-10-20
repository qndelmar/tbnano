import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'elm1\nelm10\nelm47\nelm77\nfig29\nfig45\nkiwi31\nkiwi39\nkiwi56\nkiwi74\nkiwi9\noak14\noak28\noak43\noak99\nplum11\nplum41\nplum82\nplum88\nplum96\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
