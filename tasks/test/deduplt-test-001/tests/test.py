import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[{"id": 136, "ts": 8208, "v": 45}, {"id": 262, "ts": 8119, "v": 55}, {"id": 368, "ts": 7714, "v": 83}, {"id": 378, "ts": 9608, "v": 44}, {"id": 463, "ts": 8635, "v": 81}, {"id": 553, "ts": 8821, "v": 72}, {"id": 661, "ts": 2158, "v": 84}, {"id": 835, "ts": 9315, "v": 94}, {"id": 930, "ts": 9108, "v": 10}, {"id": 934, "ts": 7979, "v": 64}, {"id": 944, "ts": 3942, "v": 78}, {"id": 977, "ts": 8615, "v": 58}]'
OUT = 'out.json'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
