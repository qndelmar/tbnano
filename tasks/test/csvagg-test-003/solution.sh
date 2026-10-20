python3 -c "
import csv
rows=[r for r in csv.DictReader(open('metrics.csv'))]
v=[float(r['reading']) for r in rows if r['sensor']=='alpha']
print({'mean':sum(v)/len(v),'sum':sum(v),'max':max(v),'count':len(v)}['max'])
" > answer.txt
