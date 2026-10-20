python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER, g TEXT);')
db.executemany('INSERT INTO t VALUES(?,?,?)', [(0, 2, 'a'), (1, 5, 'a'), (2, 8, 'b'), (3, 4, 'b'), (4, 8, 'a'), (5, 7, 'b'), (6, 8, 'b'), (7, 6, 'b'), (8, 9, 'b'), (9, 3, 'b'), (10, 5, 'b'), (11, 8, 'a'), (12, 4, 'b'), (13, 5, 'a'), (14, 4, 'a'), (15, 6, 'a'), (16, 9, 'b'), (17, 6, 'a'), (18, 1, 'a'), (19, 7, 'a'), (20, 5, 'a'), (21, 3, 'a'), (22, 1, 'b'), (23, 7, 'a'), (24, 3, 'b'), (25, 2, 'b'), (26, 9, 'a'), (27, 3, 'b'), (28, 8, 'b'), (29, 1, 'b'), (30, 6, 'b'), (31, 8, 'a'), (32, 2, 'a'), (33, 2, 'b'), (34, 3, 'b'), (35, 6, 'a'), (36, 8, 'b')])
db.commit()
PY
