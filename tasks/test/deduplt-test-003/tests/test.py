import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[{"id": 131, "ts": 7460, "v": 74}, {"id": 282, "ts": 8339, "v": 44}, {"id": 285, "ts": 9311, "v": 10}, {"id": 353, "ts": 7988, "v": 21}, {"id": 498, "ts": 7207, "v": 9}, {"id": 499, "ts": 8432, "v": 99}, {"id": 515, "ts": 8640, "v": 98}, {"id": 522, "ts": 7139, "v": 80}, {"id": 551, "ts": 4100, "v": 3}, {"id": 597, "ts": 3881, "v": 48}, {"id": 799, "ts": 2358, "v": 90}]'
OUT = 'out.json'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
