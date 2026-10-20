import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '971\n900\n775\n768\n735\n532\n532\n477\n396\n381\n357\n200\n158\n92\n66\n51\n50\n-6\n-53\n-100\n-113\n-139\n-250\n-254\n-288\n-401\n-403\n-408\n-411\n-421\n-475\n-516\n-525\n-576\n-594\n-733\n-734\n-751\n-854\n-877\n-895\n-934\n-971\n-971\n'

def test_output_file():
    p = BASE / "sorted.txt"
    assert p.exists(), "sorted.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
