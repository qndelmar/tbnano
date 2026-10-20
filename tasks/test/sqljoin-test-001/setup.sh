python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER);CREATE TABLE keep(id INTEGER);')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 10), (1, 28), (2, 65), (3, 90), (4, 17), (5, 59), (6, 56), (7, 92), (8, 93), (9, 86), (10, 24), (11, 19), (12, 38), (13, 59), (14, 73), (15, 23), (16, 93), (17, 27), (18, 62)])
db.executemany('INSERT INTO keep VALUES(?)', [(i,) for i in [0, 1, 11, 14]])
db.commit()
PY
