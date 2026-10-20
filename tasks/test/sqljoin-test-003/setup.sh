python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER);CREATE TABLE keep(id INTEGER);')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 68), (1, 77), (2, 6), (3, 83), (4, 7), (5, 94), (6, 90), (7, 4), (8, 33), (9, 31), (10, 13), (11, 93), (12, 91), (13, 83), (14, 24), (15, 23), (16, 21), (17, 36), (18, 75), (19, 95), (20, 38), (21, 69), (22, 55)])
db.executemany('INSERT INTO keep VALUES(?)', [(i,) for i in [1, 6, 8, 9, 13, 16, 20, 21, 22]])
db.commit()
PY
