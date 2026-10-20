head -3 telem.csv
python3 - <<'PY'
rows=[l.split(',') for l in open('telem.csv').read().split()[1:]]
ap=max(rows,key=lambda r:float(r[1]))
vm=max(float(r[2]) for r in rows)
open('report.txt','w').write(
 f'apogee_m={ap[1]}\nt_apogee_s={ap[0]}\nvmax_ms={vm}\n')
PY
wc -l report.txt
