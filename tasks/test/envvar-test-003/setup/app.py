import os, sys
v = os.environ.get('RUN_KEY')
if v is None:
    sys.exit('RUN_KEY not set')
print('ok-' + v)
