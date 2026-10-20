import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'ALPHA0\nCHARLIE1\nGOLF2\nCHARLIE3\nCHARLIE4\nFOXTROT5\nGOLF6\nECHO7\nFOXTROT8\nALPHA9\nCHARLIE10\nALPHA11\nFOXTROT12\nBRAVO13\nALPHA14\nECHO15\nDELTA16\n'

def test_output_file():
    p = BASE / "up.txt"
    assert p.exists(), "up.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
