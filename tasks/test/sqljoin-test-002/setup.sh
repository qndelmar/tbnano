python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER);CREATE TABLE keep(id INTEGER);')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 27), (1, 70), (2, 59), (3, 68), (4, 48), (5, 36), (6, 25), (7, 87), (8, 43), (9, 48), (10, 49), (11, 14), (12, 16), (13, 50), (14, 49), (15, 81), (16, 93), (17, 45), (18, 56), (19, 88), (20, 78), (21, 61), (22, 92), (23, 78), (24, 46)])
db.executemany('INSERT INTO keep VALUES(?)', [(i,) for i in [2, 3, 8, 9, 11, 13, 14, 15, 16, 22, 24]])
db.commit()
PY
