python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER);CREATE TABLE keep(id INTEGER);')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 39), (1, 64), (2, 99), (3, 6), (4, 27), (5, 87), (6, 41), (7, 66), (8, 84), (9, 25), (10, 4), (11, 36)])
db.executemany('INSERT INTO keep VALUES(?)', [(i,) for i in [1, 4, 6, 9]])
db.commit()
PY
