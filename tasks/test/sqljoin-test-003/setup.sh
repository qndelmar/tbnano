python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER);CREATE TABLE keep(id INTEGER);')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 85), (1, 89), (2, 10), (3, 87), (4, 99), (5, 37), (6, 58), (7, 46), (8, 13), (9, 37), (10, 56), (11, 73), (12, 44), (13, 48), (14, 48), (15, 85), (16, 91), (17, 42), (18, 43), (19, 46), (20, 91), (21, 25), (22, 92), (23, 91), (24, 64), (25, 13)])
db.executemany('INSERT INTO keep VALUES(?)', [(i,) for i in [3, 4, 6, 7, 9, 12, 14]])
db.commit()
PY
