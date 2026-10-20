import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'ECHO0\nFOXTROT1\nFOXTROT2\nCHARLIE3\nBRAVO4\nGOLF5\nFOXTROT6\nECHO7\nGOLF8\nALPHA9\nCHARLIE10\nGOLF11\nBRAVO12\nBRAVO13\nBRAVO14\nECHO15\n'

def test_output_file():
    p = BASE / "up.txt"
    assert p.exists(), "up.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
