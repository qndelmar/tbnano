import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'keep2\nkeep4\nkeep7\nkeep8\nkeep9\nkeep10\nkeep11\nkeep14\nkeep15\nkeep16\nkeep17\nkeep18\nkeep19\nkeep20\nkeep21\nkeep23\nkeep24\nkeep26\nkeep27\nkeep28\nkeep32\nkeep34\nkeep35\nkeep36\nkeep37\nkeep38\nkeep39\nkeep41\nkeep43\nkeep44\n'
OUT = 'kept.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
