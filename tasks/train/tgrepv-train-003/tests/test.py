import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'keep0\nkeep1\nkeep2\nkeep3\nkeep5\nkeep6\nkeep7\nkeep8\nkeep10\nkeep11\nkeep12\nkeep13\nkeep15\nkeep16\nkeep17\nkeep18\nkeep20\nkeep21\nkeep22\nkeep23\nkeep24\nkeep25\nkeep26\nkeep27\nkeep28\nkeep29\nkeep30\nkeep31\nkeep32\nkeep33\nkeep35\nkeep36\nkeep37\nkeep38\nkeep39\nkeep40\nkeep41\nkeep42\nkeep45\nkeep46\nkeep47\nkeep49\nkeep51\nkeep52\nkeep53\nkeep54\nkeep55\nkeep56\nkeep57\nkeep58\nkeep60\nkeep62\nkeep64\nkeep65\nkeep66\nkeep67\nkeep68\nkeep70\nkeep72\nkeep73\nkeep74\nkeep75\nkeep76\nkeep77\nkeep78\nkeep79\nkeep80\nkeep82\nkeep83\nkeep84\nkeep85\nkeep86\nkeep88\nkeep89\nkeep90\nkeep91\nkeep92\nkeep93\nkeep94\nkeep95\n'
OUT = 'kept.txt'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
