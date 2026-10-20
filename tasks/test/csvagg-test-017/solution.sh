python3 -c "
import csv
rows=[r for r in csv.DictReader(open('sales.csv'))]
v=[float(r['revenue']) for r in rows if r['region']=='south']
print({'mean':sum(v)/len(v),'sum':sum(v),'max':max(v),'count':len(v)}['max'])
" > answer.txt
