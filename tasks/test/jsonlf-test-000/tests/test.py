import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '{"kind": "event", "v": 29}\n{"kind": "event", "v": 23}\n{"kind": "event", "v": 25}\n{"kind": "event", "v": 53}\n{"kind": "event", "v": 29}\n{"kind": "event", "v": 3}\n{"kind": "event", "v": 66}\n{"kind": "event", "v": 68}\n{"kind": "event", "v": 15}\n{"kind": "event", "v": 98}\n{"kind": "event", "v": 93}\n{"kind": "event", "v": 64}\n{"kind": "event", "v": 95}\n'
OUT = 'out.jsonl'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
