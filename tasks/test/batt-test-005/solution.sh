python3 - <<'PY' > answer.txt
import json, math
p = json.load(open('params.json'))
print(p['mah']/1000*p['c_rating'])
PY
