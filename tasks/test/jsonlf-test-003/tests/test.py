import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '{"kind": "alarm", "v": 99}\n{"kind": "alarm", "v": 61}\n{"kind": "alarm", "v": 75}\n{"kind": "alarm", "v": 77}\n{"kind": "alarm", "v": 96}\n{"kind": "alarm", "v": 72}\n{"kind": "alarm", "v": 93}\n'
OUT = 'out.jsonl'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
