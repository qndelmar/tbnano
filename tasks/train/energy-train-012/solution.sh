python3 - <<'EOF'
import csv
rows=list(csv.DictReader(open('rail.csv')))
t=[float(r['t_s']) for r in rows]
p=[float(r['power_w']) for r in rows]
e=sum((p[i]+p[i+1])/2*(t[i+1]-t[i]) for i in range(len(t)-1))/3600
open('answer.txt','w').write(str(e))
EOF
