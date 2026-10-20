python3 -c "
import csv
rows=[r for r in csv.DictReader(open('records.csv'))]
v=[float(r['duration_s']) for r in rows if r['fleet']=='alpha']
print({'mean':sum(v)/len(v),'sum':sum(v),'max':max(v),'count':len(v)}['mean'])
" > answer.txt
