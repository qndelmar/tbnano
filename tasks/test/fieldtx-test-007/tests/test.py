import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'ALPHA0\nGOLF1\nALPHA2\nDELTA3\nGOLF4\nFOXTROT5\nGOLF6\nGOLF7\nALPHA8\nFOXTROT9\nALPHA10\nCHARLIE11\nCHARLIE12\nALPHA13\nCHARLIE14\nDELTA15\nCHARLIE16\nCHARLIE17\nGOLF18\nDELTA19\n'

def test_output_file():
    p = BASE / "up.txt"
    assert p.exists(), "up.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
