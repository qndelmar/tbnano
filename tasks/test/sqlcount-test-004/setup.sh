python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER, g TEXT);')
db.executemany('INSERT INTO t VALUES(?,?,?)', [(0, 6, 'a'), (1, 2, 'b'), (2, 4, 'b'), (3, 6, 'b'), (4, 1, 'a'), (5, 7, 'b'), (6, 6, 'a'), (7, 3, 'b'), (8, 1, 'b'), (9, 1, 'a'), (10, 8, 'a'), (11, 4, 'b'), (12, 2, 'b'), (13, 6, 'a'), (14, 5, 'b'), (15, 9, 'b'), (16, 3, 'a'), (17, 8, 'a'), (18, 2, 'b'), (19, 8, 'b'), (20, 4, 'a'), (21, 3, 'b'), (22, 6, 'a'), (23, 3, 'a'), (24, 9, 'a'), (25, 3, 'b'), (26, 7, 'b'), (27, 7, 'b'), (28, 3, 'a'), (29, 8, 'a'), (30, 7, 'b'), (31, 4, 'b'), (32, 6, 'b'), (33, 7, 'a'), (34, 5, 'a'), (35, 1, 'a'), (36, 8, 'a'), (37, 8, 'b')])
db.commit()
PY
