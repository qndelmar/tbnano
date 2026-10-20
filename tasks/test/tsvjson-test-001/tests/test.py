import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '[{"id": 0, "name": "n0"}, {"id": 1, "name": "n1"}, {"id": 2, "name": "n2"}, {"id": 3, "name": "n3"}, {"id": 4, "name": "n4"}, {"id": 5, "name": "n5"}, {"id": 6, "name": "n6"}, {"id": 7, "name": "n7"}, {"id": 8, "name": "n8"}, {"id": 9, "name": "n9"}, {"id": 10, "name": "n10"}, {"id": 11, "name": "n11"}, {"id": 12, "name": "n12"}, {"id": 13, "name": "n13"}, {"id": 14, "name": "n14"}, {"id": 15, "name": "n15"}, {"id": 16, "name": "n16"}, {"id": 17, "name": "n17"}, {"id": 18, "name": "n18"}, {"id": 19, "name": "n19"}, {"id": 20, "name": "n20"}]'
OUT = 'out.json'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
