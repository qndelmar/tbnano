import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = '998\n996\n974\n857\n823\n703\n688\n657\n640\n628\n568\n545\n335\n257\n238\n220\n172\n120\n107\n53\n-78\n-104\n-108\n-129\n-233\n-251\n-274\n-321\n-366\n-547\n-548\n-592\n-678\n-757\n-786\n-844\n'

def test_output_file():
    p = BASE / "sorted.txt"
    assert p.exists(), "sorted.txt missing"
    assert p.read_text() == EXPECTED, f"content mismatch"
