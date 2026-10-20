import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '935\n908\n843\n790\n755\n736\n719\n678\n668\n642\n550\n474\n386\n353\n345\n283\n253\n218\n119\n113\n108\n94\n12\n6\n-29\n-60\n-63\n-117\n-143\n-163\n-228\n-241\n-272\n-301\n-319\n-371\n-377\n-392\n-410\n-422\n-430\n-466\n-528\n-557\n-587\n-632\n-644\n-651\n-671\n-690\n-832\n-938\n-955\n'

def test_output_file():
    p = BASE / "sorted.txt"
    assert p.exists(), "sorted.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
