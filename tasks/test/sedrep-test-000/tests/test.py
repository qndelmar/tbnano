import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'v2=old\nk1=v1\nk2=v2\nv2=dev\nk4=v4\nk5=v5\nv2=x\nk7=v7\nk8=v8\nv2=old\nk10=v10\nk11=v11\nv2=old\n'
OUT = 'cfg_fixed.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
