import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'elm18\nelm35\nelm73\nelm78\nelm88\nfig29\nfig34\nfig52\nfig7\nfig77\nfig86\nkiwi79\nkiwi96\noak30\noak36\noak67\nplum17\nplum17\nplum54\nplum67\nplum8\nplum97\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
