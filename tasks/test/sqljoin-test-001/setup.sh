python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER);CREATE TABLE keep(id INTEGER);')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 27), (1, 20), (2, 86), (3, 53), (4, 61), (5, 46), (6, 72), (7, 54), (8, 2), (9, 61), (10, 83), (11, 3), (12, 48), (13, 83), (14, 53), (15, 47), (16, 97)])
db.executemany('INSERT INTO keep VALUES(?)', [(i,) for i in [0, 2, 4, 7, 12, 13, 14, 15]])
db.commit()
PY
