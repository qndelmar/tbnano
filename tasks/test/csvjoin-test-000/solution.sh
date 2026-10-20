python3 - <<'PY'
u={l.split(',')[0]:l.split(',',1)[1] for l in open('users.csv').read().split()}
o={l.split(',')[0]:l.split(',',1)[1].strip() for l in open('orders.csv').read().split()}
open('joined.csv','w').write(
 ''.join(f'{i},{u[i]},{o[i]}\n' for i in sorted(u,key=int)))
PY
head joined.csv
