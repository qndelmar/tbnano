import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'keep1\nkeep2\nkeep3\nkeep5\nkeep6\nkeep7\nkeep8\nkeep9\nkeep10\nkeep11\nkeep12\nkeep14\nkeep15\nkeep16\nkeep19\nkeep20\nkeep21\nkeep22\nkeep23\nkeep25\nkeep26\nkeep27\nkeep28\nkeep30\nkeep31\nkeep32\nkeep33\nkeep34\nkeep35\nkeep36\nkeep37\nkeep39\nkeep40\nkeep41\nkeep42\nkeep44\nkeep46\nkeep48\nkeep49\nkeep50\nkeep51\nkeep52\nkeep53\nkeep54\nkeep55\nkeep56\nkeep57\nkeep58\nkeep59\nkeep60\nkeep61\nkeep62\nkeep63\nkeep65\nkeep66\nkeep67\nkeep68\nkeep69\nkeep70\nkeep72\nkeep73\nkeep74\nkeep75\nkeep76\nkeep77\nkeep78\nkeep81\nkeep82\nkeep84\nkeep85\nkeep87\nkeep89\nkeep91\nkeep93\n'
OUT = 'kept.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
