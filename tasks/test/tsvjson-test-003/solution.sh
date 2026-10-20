python3 - <<'PY'
import csv, json
rows=list(csv.DictReader(open('in.tsv'), delimiter='\t'))
out=[{'id': int(r['id']), 'name': r['name']} for r in rows]
open('out.json','w').write(json.dumps(out))
PY
