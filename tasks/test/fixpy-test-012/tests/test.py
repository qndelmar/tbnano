import os, sys
sys.path.insert(0, os.environ.get('TBNANO_TASK_DIR', '/task'))
from calc import clamp

def test_clamp():
    assert abs(clamp(5, 0, 10) - 5) < 1e-4, f'{ clamp(5, 0, 10) } != 5'
    assert abs(clamp(15, 0, 10) - 10) < 1e-4, f'{ clamp(15, 0, 10) } != 10'
    assert abs(clamp(-3, 0, 10) - 0) < 1e-4, f'{ clamp(-3, 0, 10) } != 0'
    assert abs(clamp(11, 0, 10) - 10) < 1e-4, f'{ clamp(11, 0, 10) } != 10'
    assert abs(clamp(7, 2, 8) - 7) < 1e-4, f'{ clamp(7, 2, 8) } != 7'
