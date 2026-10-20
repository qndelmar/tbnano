import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'prod=old\nk1=v1\nk2=v2\nprod=x\nk4=v4\nk5=v5\nprod=old\nk7=v7\nk8=v8\nprod=old\nk10=v10\nk11=v11\nprod=old\nk13=v13\n'
OUT = 'cfg_fixed.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
