import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'elm31\nelm85\nfig55\nfig6\nfig63\nfig75\nfig79\nfig8\nfig8\nfig91\nkiwi12\nkiwi69\nkiwi76\noak24\noak50\noak6\nplum45\nplum56\nplum85\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
