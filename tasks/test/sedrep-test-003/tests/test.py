import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'prod=x\nk1=v1\nk2=v2\nprod=dev\nk4=v4\nk5=v5\nprod=dev\nk7=v7\nk8=v8\nprod=dev\nk10=v10\n'
OUT = 'cfg_fixed.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
