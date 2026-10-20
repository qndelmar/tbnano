import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '129,u77,33\n185,u78,27\n229,u51,28\n239,u28,16\n299,u46,38\n427,u74,28\n509,u65,13\n625,u13,5\n637,u41,45\n686,u33,8\n764,u79,24\n795,u83,6\n807,u12,21\n915,u33,25\n'
OUT = 'joined.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
