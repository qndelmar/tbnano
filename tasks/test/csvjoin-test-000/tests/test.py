import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '128,u61,50\n142,u55,50\n193,u15,34\n202,u92,48\n224,u90,35\n329,u96,31\n402,u41,48\n432,u33,8\n519,u73,8\n549,u69,48\n557,u32,44\n602,u39,41\n630,u72,38\n644,u42,4\n660,u78,48\n721,u38,5\n764,u42,37\n894,u60,24\n925,u63,9\n958,u86,23\n988,u36,41\n'
OUT = 'joined.csv'

def test_file_present():
    assert (BASE / OUT).exists(), f"{OUT} missing"

def test_content():
    assert (BASE / OUT).read_text() == EXPECTED
