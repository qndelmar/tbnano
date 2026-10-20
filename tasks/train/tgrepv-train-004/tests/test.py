import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'keep0\nkeep2\nkeep3\nkeep4\nkeep5\nkeep9\nkeep12\nkeep13\nkeep14\nkeep15\nkeep17\nkeep18\nkeep19\nkeep20\nkeep21\nkeep22\nkeep23\nkeep25\nkeep26\nkeep28\nkeep29\nkeep30\nkeep32\nkeep33\nkeep35\nkeep37\nkeep39\nkeep40\nkeep43\nkeep44\nkeep45\nkeep46\nkeep48\nkeep49\nkeep50\nkeep52\nkeep53\nkeep55\nkeep57\nkeep58\nkeep59\nkeep61\nkeep63\nkeep64\n'
OUT = 'kept.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
