import os, sys
sys.path.insert(0, os.environ.get('TBNANO_TASK_DIR', '/task'))
from utils import moving_average

def test_moving_average():
    assert moving_average((1, 2, 3, 4), 2) == [1.5, 2.5, 3.5], f'{ moving_average((1, 2, 3, 4), 2) } != [1.5, 2.5, 3.5]'
    assert moving_average((1, 2, 3, 4, 5), 3) == [2.0, 3.0, 4.0], f'{ moving_average((1, 2, 3, 4, 5), 3) } != [2.0, 3.0, 4.0]'
