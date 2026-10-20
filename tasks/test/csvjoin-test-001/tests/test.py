import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '130,u81,8\n143,u18,39\n204,u27,47\n207,u67,15\n240,u26,11\n393,u73,7\n532,u85,28\n595,u92,43\n680,u81,37\n728,u51,9\n737,u55,1\n755,u71,38\n803,u28,36\n871,u76,11\n924,u55,20\n973,u42,45\n'
OUT = 'joined.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
