python3 - <<'PY' > answer.txt
import json, math
p = json.load(open('params.json'))
print(p['fuel_kg']/p['burn_rate_kgs'])
PY
