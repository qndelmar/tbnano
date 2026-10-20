import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[{"id": 195, "ts": 5873, "v": 86}, {"id": 319, "ts": 8302, "v": 34}, {"id": 329, "ts": 8357, "v": 65}, {"id": 441, "ts": 9405, "v": 21}, {"id": 451, "ts": 4815, "v": 98}, {"id": 527, "ts": 7276, "v": 71}, {"id": 555, "ts": 5693, "v": 42}, {"id": 628, "ts": 9880, "v": 51}, {"id": 711, "ts": 6224, "v": 44}, {"id": 731, "ts": 9692, "v": 6}, {"id": 861, "ts": 5034, "v": 30}, {"id": 879, "ts": 6119, "v": 97}, {"id": 903, "ts": 9530, "v": 42}, {"id": 963, "ts": 8011, "v": 66}]'
OUT = 'out.json'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
