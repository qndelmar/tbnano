import os, sys
sys.path.insert(0, os.environ.get('TBNANO_TASK_DIR', '/task'))
from ops import area_circle

def test_area_circle():
    assert abs(area_circle(2) - 12.56636) < 1e-4, f'{ area_circle(2) } != 12.56636'
    assert abs(area_circle(5) - 78.53975) < 1e-4, f'{ area_circle(5) } != 78.53975'
    assert abs(area_circle(1) - 3.14159) < 1e-4, f'{ area_circle(1) } != 3.14159'
    assert abs(area_circle(3.5) - 38.484477) < 1e-4, f'{ area_circle(3.5) } != 38.484477'
