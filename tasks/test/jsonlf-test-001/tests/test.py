import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '{"kind": "alarm", "v": 19}\n{"kind": "alarm", "v": 54}\n{"kind": "alarm", "v": 6}\n{"kind": "alarm", "v": 65}\n{"kind": "alarm", "v": 2}\n{"kind": "alarm", "v": 8}\n{"kind": "alarm", "v": 82}\n{"kind": "alarm", "v": 87}\n{"kind": "alarm", "v": 35}\n'
OUT = 'out.jsonl'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
