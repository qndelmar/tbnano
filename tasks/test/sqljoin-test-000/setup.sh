python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER);CREATE TABLE keep(id INTEGER);')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 72), (1, 8), (2, 89), (3, 9), (4, 50), (5, 59), (6, 27), (7, 60), (8, 81), (9, 67), (10, 83), (11, 5), (12, 3)])
db.executemany('INSERT INTO keep VALUES(?)', [(i,) for i in [2, 4, 5, 8, 9, 11]])
db.commit()
PY
