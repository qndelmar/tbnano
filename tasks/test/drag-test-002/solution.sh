python3 - <<'PY' > answer.txt
import json, math
p = json.load(open('params.json'))
print(0.5*1.225*p['v_ms']**2*p['cd']*p['area_m2'])
PY
