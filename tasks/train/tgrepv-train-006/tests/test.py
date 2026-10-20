import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'keep0\nkeep1\nkeep2\nkeep3\nkeep4\nkeep5\nkeep6\nkeep7\nkeep8\nkeep9\nkeep10\nkeep11\nkeep12\nkeep13\nkeep15\nkeep16\nkeep17\nkeep18\nkeep21\nkeep22\nkeep23\nkeep24\nkeep25\nkeep27\nkeep28\nkeep29\nkeep30\nkeep31\nkeep32\nkeep33\nkeep34\nkeep36\nkeep37\nkeep38\nkeep39\nkeep40\nkeep41\nkeep42\nkeep43\nkeep45\nkeep46\nkeep48\nkeep49\n'
OUT = 'kept.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
