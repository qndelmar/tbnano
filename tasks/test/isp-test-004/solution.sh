python3 - <<'PY' > answer.txt
import json, math
p = json.load(open('params.json'))
print(p['thrust_n']*p['burn_s']/(p['prop_kg']*9.81))
PY
