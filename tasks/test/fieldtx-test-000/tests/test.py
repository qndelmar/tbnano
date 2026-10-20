import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'blue\ncyan\ngreen\nred\n'

def test_output_file():
    p = BASE / "uniq.txt"
    assert p.exists(), "uniq.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
