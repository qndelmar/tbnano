python3 - <<'PY' > answer.txt
import json, math
p = json.load(open('params.json'))
print(0.5*p['mass_kg']*((p['thrust_n']-p['mass_kg']*9.81)/p['mass_kg']*p['burn_s'])**2)
PY
