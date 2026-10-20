python3 - <<'PY' > answer.txt
import json, math
p = json.load(open('params.json'))
print(p['value']*p['factor'])
PY
