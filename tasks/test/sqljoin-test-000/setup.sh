python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER);CREATE TABLE keep(id INTEGER);')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 74), (1, 59), (2, 52), (3, 33), (4, 2), (5, 7), (6, 27), (7, 60), (8, 19), (9, 68), (10, 72), (11, 83), (12, 35), (13, 26), (14, 17), (15, 41), (16, 33)])
db.executemany('INSERT INTO keep VALUES(?)', [(i,) for i in [3, 12, 14, 15, 16]])
db.commit()
PY
