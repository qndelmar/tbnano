import os, sys
sys.path.insert(0, os.environ.get('TBNANO_TASK_DIR', '/task'))
from compute import km_to_miles

def test_km_to_miles():
    assert abs(km_to_miles(10) - 6.21371) < 1e-4, f'{ km_to_miles(10) } != 6.21371'
    assert abs(km_to_miles(100) - 62.1371) < 1e-4, f'{ km_to_miles(100) } != 62.1371'
    assert abs(km_to_miles(42) - 26.097582) < 1e-4, f'{ km_to_miles(42) } != 26.097582'
