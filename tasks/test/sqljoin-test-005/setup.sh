python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER);CREATE TABLE keep(id INTEGER);')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 94), (1, 26), (2, 56), (3, 45), (4, 46), (5, 17), (6, 82), (7, 86), (8, 49), (9, 9), (10, 5), (11, 66), (12, 2), (13, 2), (14, 22), (15, 44), (16, 99), (17, 47), (18, 66), (19, 61), (20, 31), (21, 1), (22, 32), (23, 22), (24, 82), (25, 48), (26, 28), (27, 24), (28, 14), (29, 42)])
db.executemany('INSERT INTO keep VALUES(?)', [(i,) for i in [0, 3, 5, 6, 8, 15, 19, 21, 23, 29]])
db.commit()
PY
