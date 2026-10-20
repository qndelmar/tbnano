import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'ECHO0\nECHO1\nECHO2\nALPHA3\nDELTA4\nGOLF5\nBRAVO6\nECHO7\nALPHA8\nCHARLIE9\nBRAVO10\nFOXTROT11\nBRAVO12\nALPHA13\nBRAVO14\n'

def test_output_file():
    p = BASE / "up.txt"
    assert p.exists(), "up.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
