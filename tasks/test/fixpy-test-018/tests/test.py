import os, sys
sys.path.insert(0, os.environ.get('TBNANO_TASK_DIR', '/task'))
from utils import sum_evens

def test_sum_evens():
    assert abs(sum_evens((1, 2, 3, 4, 5, 6)) - 12) < 1e-4, f'{ sum_evens((1, 2, 3, 4, 5, 6)) } != 12'
    assert abs(sum_evens((2, 4, 7, 9, 10)) - 16) < 1e-4, f'{ sum_evens((2, 4, 7, 9, 10)) } != 16'
