import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'GOLF0\nECHO1\nGOLF2\nDELTA3\nFOXTROT4\nECHO5\nECHO6\nALPHA7\nFOXTROT8\nALPHA9\n'

def test_output_file():
    p = BASE / "up.txt"
    assert p.exists(), "up.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
