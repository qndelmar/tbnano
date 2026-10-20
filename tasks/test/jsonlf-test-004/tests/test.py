import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '{"kind": "metric", "v": 90}\n{"kind": "metric", "v": 90}\n{"kind": "metric", "v": 99}\n{"kind": "metric", "v": 53}\n{"kind": "metric", "v": 53}\n{"kind": "metric", "v": 91}\n{"kind": "metric", "v": 98}\n{"kind": "metric", "v": 25}\n{"kind": "metric", "v": 38}\n{"kind": "metric", "v": 55}\n{"kind": "metric", "v": 63}\n{"kind": "metric", "v": 94}\n{"kind": "metric", "v": 51}\n{"kind": "metric", "v": 75}\n'
OUT = 'out.jsonl'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
