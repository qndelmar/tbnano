python3 - <<'PY' > answer.txt
import json, math
p = json.load(open('params.json'))
print(p['mach']*331.3*math.sqrt(1+p['temp_c']/273.15))
PY
