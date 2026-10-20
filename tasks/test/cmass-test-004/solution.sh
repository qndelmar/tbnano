head -3 thrust.csv
python3 - <<'PY' > answer.txt
rows=[l.split(',') for l in open('parts.csv').read().split()]
M=sum(float(m) for m,_ in rows)
print(sum(float(m)*float(x) for m,x in rows)/M)
PY
