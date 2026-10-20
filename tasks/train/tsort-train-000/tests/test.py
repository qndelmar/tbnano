import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'elm48\nelm5\nfig42\nfig67\nfig74\nkiwi12\nkiwi72\nkiwi74\nkiwi80\nkiwi86\noak14\noak44\noak52\noak82\noak95\nplum41\nplum42\nplum51\nplum71\nplum85\nplum98\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
