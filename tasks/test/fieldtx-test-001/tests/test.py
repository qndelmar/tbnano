import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'CHARLIE0\nFOXTROT1\nCHARLIE2\nECHO3\nGOLF4\nGOLF5\nBRAVO6\nFOXTROT7\nGOLF8\nECHO9\nDELTA10\n'

def test_output_file():
    p = BASE / "up.txt"
    assert p.exists(), "up.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
