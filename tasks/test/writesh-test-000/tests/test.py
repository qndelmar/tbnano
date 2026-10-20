import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 'id,x,y\n26,999,724\n94,364,121\n108,327,185\n137,733,553\n138,348,767\n184,281,14\n213,229,442\n237,932,684\n242,319,874\n250,54,70\n287,934,287\n310,76,256\n386,866,450\n403,234,874\n498,964,366\n504,68,260\n631,132,882\n652,569,702\n710,780,365\n775,923,434\n810,416,441\n829,739,272\n846,450,658\n874,703,501\n904,464,958\n906,836,354\n917,901,252\n942,901,896\n992,23,513\n999,412,377\n'

def test_merged():
    p = BASE / "merged.csv"
    assert p.exists(), "merged.csv missing"
    assert p.read_text() == EXPECTED
