head -3 thrust.csv
python3 - <<'PY' > answer.txt
rows=[l.split(',') for l in open('thrust.csv').read().split()[1:]]
v=[float(r[1]) for r in rows]
print(sum((v[i]+v[i+1])/2*0.01 for i in range(len(v)-1)))
PY
