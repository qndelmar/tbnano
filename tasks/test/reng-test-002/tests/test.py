import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'zulu\nzulu\nkilo\nhotel\nion\n'
OUT = 'data.done'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
def test_old_gone():
    assert not (BASE / "data.log").exists(), "data.log still exists"
