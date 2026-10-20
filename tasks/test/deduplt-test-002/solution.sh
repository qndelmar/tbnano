python3 -c 'import json;print(len(json.load(open("events.json"))))'
python3 - <<'PY'
import json
rows=json.load(open('events.json'))
latest={}
for r in rows:
    if r['id'] not in latest or r['ts']>latest[r['id']]['ts']:
        latest[r['id']]=r
out=sorted(latest.values(), key=lambda r: r['id'])
open('out.json','w').write(json.dumps(out))
PY
