python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER);CREATE TABLE keep(id INTEGER);')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 26), (1, 47), (2, 51), (3, 32), (4, 28), (5, 97), (6, 47), (7, 79), (8, 3), (9, 65), (10, 87), (11, 8), (12, 62), (13, 97), (14, 85), (15, 88), (16, 37), (17, 85)])
db.executemany('INSERT INTO keep VALUES(?)', [(i,) for i in [5, 6, 12, 13, 14, 16]])
db.commit()
PY
