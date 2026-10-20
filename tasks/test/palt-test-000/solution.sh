python3 - <<'PY' > answer.txt
import json, math
p = json.load(open('params.json'))
print(44330*(1-(p['pressure_hpa']/1013.25)**0.1903))
PY
