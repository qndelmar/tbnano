python3 - <<'PY' > answer.txt
import json, math
p = json.load(open('params.json'))
print(p['isp_s']*9.81*math.log(p['m0_kg']/p['mf_kg']))
PY
