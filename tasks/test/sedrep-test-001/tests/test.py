import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'prod=x\nk1=v1\nk2=v2\nprod=old\nk4=v4\nk5=v5\nprod=old\nk7=v7\nk8=v8\nprod=dev\nk10=v10\nk11=v11\nprod=x\nk13=v13\nk14=v14\nprod=dev\nk16=v16\nk17=v17\nprod=dev\n'
OUT = 'cfg_fixed.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
