import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '792\n782\n774\n704\n618\n519\n484\n368\n359\n352\n303\n68\n57\n-18\n-38\n-56\n-94\n-196\n-293\n-339\n-402\n-421\n-448\n-449\n-494\n-803\n-876\n-907\n-924\n-971\n'

def test_output_file():
    p = BASE / "sorted.txt"
    assert p.exists(), "sorted.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
