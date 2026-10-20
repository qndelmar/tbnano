import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[{"id": 198, "ts": 7256, "v": 86}, {"id": 223, "ts": 5379, "v": 71}, {"id": 549, "ts": 9152, "v": 34}, {"id": 618, "ts": 7751, "v": 90}, {"id": 645, "ts": 9036, "v": 96}, {"id": 667, "ts": 3939, "v": 89}, {"id": 685, "ts": 2401, "v": 90}, {"id": 775, "ts": 3765, "v": 5}, {"id": 778, "ts": 9447, "v": 97}, {"id": 779, "ts": 2240, "v": 99}]'
OUT = 'out.json'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
