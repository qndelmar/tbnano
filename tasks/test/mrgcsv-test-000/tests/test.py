import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '265,3,63\n268,8,53\n279,3,75\n313,5,64\n321,5,34\n345,2,79\n464,9,44\n534,5,36\n542,1,80\n582,2,87\n590,2,76\n661,6,69\n678,7,23\n680,2,74\n823,1,27\n971,6,77\n972,2,85\n'
OUT = 'merged.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
