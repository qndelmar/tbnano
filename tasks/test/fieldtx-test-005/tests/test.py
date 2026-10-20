import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'CHARLIE0\nFOXTROT1\nBRAVO2\nALPHA3\nFOXTROT4\nALPHA5\nDELTA6\nBRAVO7\nDELTA8\n'

def test_output_file():
    p = BASE / "up.txt"
    assert p.exists(), "up.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
