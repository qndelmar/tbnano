python3 - <<'PY'
import sqlite3
db = sqlite3.connect('m.db')
db.execute('CREATE TABLE t(id INTEGER, v INTEGER)')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 220), (1, 59), (2, 774), (3, 887), (4, 26), (5, 179), (6, 392), (7, 932), (8, 765), (9, 486), (10, 347), (11, 693), (12, 165), (13, 501), (14, 902)])
db.commit()
PY
