python3 - <<'PY' > answer.txt
import json, math
p = json.load(open('params.json'))
print(math.sqrt(3.986e14/(6371e3+p['alt_km']*1e3)))
PY
