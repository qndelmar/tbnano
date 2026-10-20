python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER);CREATE TABLE keep(id INTEGER);')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 15), (1, 93), (2, 35), (3, 89), (4, 95), (5, 12), (6, 62), (7, 25), (8, 97), (9, 65), (10, 76), (11, 68), (12, 49), (13, 79), (14, 8), (15, 94), (16, 50), (17, 87), (18, 16), (19, 29), (20, 53), (21, 85), (22, 27), (23, 7), (24, 90), (25, 97), (26, 97), (27, 14), (28, 89), (29, 92)])
db.executemany('INSERT INTO keep VALUES(?)', [(i,) for i in [2, 4, 6, 8, 10, 11, 15, 17, 18, 23, 28]])
db.commit()
PY
