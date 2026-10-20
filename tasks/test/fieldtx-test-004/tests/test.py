import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '991\n961\n756\n747\n735\n711\n703\n665\n609\n582\n569\n555\n521\n503\n477\n404\n301\n260\n235\n104\n40\n21\n0\n-7\n-7\n-44\n-59\n-62\n-84\n-86\n-106\n-171\n-213\n-300\n-334\n-336\n-356\n-356\n-373\n-374\n-381\n-392\n-430\n-479\n-552\n-605\n-631\n-744\n-812\n-870\n-934\n-938\n-995\n'

def test_output_file():
    p = BASE / "sorted.txt"
    assert p.exists(), "sorted.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
