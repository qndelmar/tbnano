import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '102,u73,28\n219,u24,17\n224,u75,38\n378,u94,22\n379,u50,44\n419,u66,18\n435,u87,38\n496,u82,4\n585,u41,29\n611,u62,35\n616,u10,11\n739,u82,40\n764,u64,48\n776,u89,44\n782,u47,5\n863,u48,6\n866,u59,39\n920,u46,21\n959,u56,16\n976,u83,35\n'
OUT = 'joined.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
