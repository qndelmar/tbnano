python3 -c "
import csv
rows=[r for r in csv.DictReader(open('ledger.csv'))]
v=[float(r['revenue']) for r in rows if r['region']=='north']
print({'mean':sum(v)/len(v),'sum':sum(v),'max':max(v),'count':len(v)}['sum'])
" > answer.txt
