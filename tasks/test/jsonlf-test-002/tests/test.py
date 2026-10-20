import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '{"kind": "event", "v": 11}\n{"kind": "event", "v": 79}\n{"kind": "event", "v": 89}\n{"kind": "event", "v": 48}\n{"kind": "event", "v": 43}\n{"kind": "event", "v": 51}\n{"kind": "event", "v": 90}\n{"kind": "event", "v": 61}\n{"kind": "event", "v": 69}\n{"kind": "event", "v": 80}\n{"kind": "event", "v": 13}\n'
OUT = 'out.jsonl'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
