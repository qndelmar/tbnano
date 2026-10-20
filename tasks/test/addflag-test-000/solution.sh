cat > echo.py <<'PY'
import sys
args = sys.argv[1:]
if args and args[0] == '-u':
    print(' '.join(args[1:]).upper())
else:
    print(' '.join(args))
PY
python3 echo.py -u hi there > out.txt
