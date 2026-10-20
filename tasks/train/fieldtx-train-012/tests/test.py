import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'GOLF0\nDELTA1\nALPHA2\nALPHA3\nBRAVO4\nDELTA5\nECHO6\nGOLF7\nFOXTROT8\nGOLF9\nDELTA10\nCHARLIE11\nGOLF12\nECHO13\nALPHA14\nDELTA15\nDELTA16\nFOXTROT17\nGOLF18\nGOLF19\nFOXTROT20\nECHO21\n'

def test_output_file():
    p = BASE / "up.txt"
    assert p.exists(), "up.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
