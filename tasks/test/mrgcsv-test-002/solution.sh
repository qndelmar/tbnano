cat > merge.py <<'PY'
a={l.split(',')[0]: l.split(',')[1] for l in open('a.csv').read().split()}
b={l.split(',')[0]: l.split(',')[1] for l in open('b.csv').read().split()}
out=['%s,%s,%s' % (k, a[k], b[k]) for k in sorted(a, key=int)]
open('merged.csv','w').write('\n'.join(out)+'\n')
PY
python3 merge.py
wc -l merged.csv a.csv
