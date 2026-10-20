import os
from pathlib import Path
p = Path('conf/settings.ini')
v = [l.split('=',1)[1].strip() for l in p.read_text().splitlines() if l.startswith('token=')][0]
print(v)
