python3 - <<'PY' > answer.txt
import math
kv=dict(l.split('=') for l in open('gps.txt').read().split())
la=float(kv['lat1']);lo1=float(kv['lon1']);lo2=float(kv['lon2'])
dlon=math.radians(lo2-lo1)
a=math.cos(math.radians(la))**2*math.sin(dlon/2)**2
print(2*6371*math.asin(math.sqrt(a)))
PY
