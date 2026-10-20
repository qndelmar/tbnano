import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '964\n952\n924\n897\n861\n744\n647\n598\n506\n490\n429\n418\n417\n340\n135\n28\n-75\n-97\n-135\n-479\n-572\n-581\n-592\n-641\n-841\n-965\n'
OUT = 'sorted.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
