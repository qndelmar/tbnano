import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'DELTA0\nBRAVO1\nDELTA2\nFOXTROT3\nALPHA4\nALPHA5\nGOLF6\nBRAVO7\nBRAVO8\nBRAVO9\nBRAVO10\nGOLF11\n'

def test_output_file():
    p = BASE / "up.txt"
    assert p.exists(), "up.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
