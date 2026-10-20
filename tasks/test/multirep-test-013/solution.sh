python3 - <<'EOF'
import csv, json
rows=list(csv.DictReader(open('flight.csv')))
t=[float(r['t_s']) for r in rows]
a=[float(r['alt_ft']) for r in rows]
m=json.load(open('meta.json'))
rep=(f"duration_s={t[-1]-t[0]:g}\n"
     f"max_alt_m={max(a)*0.3048}\n"
     f"fuel_kg={(m['fuel_start_lbs']-m['fuel_end_lbs'])*0.45359237}\n")
open('report.txt','w').write(rep)
EOF
