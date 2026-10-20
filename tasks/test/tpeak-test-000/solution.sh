head -3 telem.csv
python3 - <<'PY' > answer.txt
rows=[l.split(',') for l in open('telem.csv').read().split()[1:]]
print(max(rows, key=lambda r: float(r[1]))[0])
PY
