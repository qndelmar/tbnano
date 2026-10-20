python3 - <<'PY' > answer.txt
import csv
r=list(csv.DictReader(open('sales.csv')))
v=[float(x['id']) for x in r]
print({'sum':sum(v),'avg':sum(v)/len(v),'count':len(v)}['count'])
PY
