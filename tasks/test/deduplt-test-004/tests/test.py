import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[{"id": 133, "ts": 8825, "v": 13}, {"id": 239, "ts": 6110, "v": 95}, {"id": 332, "ts": 1560, "v": 22}, {"id": 333, "ts": 2271, "v": 69}, {"id": 350, "ts": 9329, "v": 1}, {"id": 389, "ts": 2520, "v": 55}, {"id": 399, "ts": 9609, "v": 97}, {"id": 434, "ts": 6966, "v": 75}, {"id": 603, "ts": 9794, "v": 56}, {"id": 884, "ts": 6614, "v": 71}, {"id": 897, "ts": 8880, "v": 91}, {"id": 918, "ts": 5359, "v": 33}, {"id": 942, "ts": 2800, "v": 63}, {"id": 967, "ts": 3391, "v": 83}, {"id": 983, "ts": 7820, "v": 28}]'
OUT = 'out.json'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
