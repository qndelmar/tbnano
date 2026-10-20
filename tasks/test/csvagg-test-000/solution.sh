python3 -c "
import csv
rows=[r for r in csv.DictReader(open('flights.csv'))]
v=[float(r['duration_s']) for r in rows if r['fleet']=='beta']
print({'mean':sum(v)/len(v),'sum':sum(v),'max':max(v),'count':len(v)}['max'])
" > answer.txt
