python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER);CREATE TABLE keep(id INTEGER);')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 37), (1, 34), (2, 30), (3, 19), (4, 15), (5, 84), (6, 57), (7, 17), (8, 93), (9, 24), (10, 48), (11, 31), (12, 26), (13, 95), (14, 72), (15, 60), (16, 74), (17, 11), (18, 89), (19, 85), (20, 94), (21, 31), (22, 29), (23, 56), (24, 61), (25, 96), (26, 43), (27, 70)])
db.executemany('INSERT INTO keep VALUES(?)', [(i,) for i in [9, 10, 20, 22, 27]])
db.commit()
PY
