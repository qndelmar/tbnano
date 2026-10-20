import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'k0=v0\nk1=v1\nk2=v2\nk3=v3\nk4=v4\nk5=v5\ndone=165\n'
OUT = 'cfg.ini'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
