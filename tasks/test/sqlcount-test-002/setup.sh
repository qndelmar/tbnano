python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER, g TEXT);')
db.executemany('INSERT INTO t VALUES(?,?,?)', [(0, 5, 'b'), (1, 1, 'a'), (2, 5, 'b'), (3, 5, 'a'), (4, 7, 'a'), (5, 6, 'a'), (6, 9, 'a'), (7, 1, 'b'), (8, 9, 'b'), (9, 5, 'b'), (10, 3, 'b'), (11, 7, 'b'), (12, 9, 'a'), (13, 2, 'b'), (14, 9, 'b'), (15, 3, 'b'), (16, 2, 'b'), (17, 9, 'a'), (18, 4, 'a'), (19, 7, 'b'), (20, 5, 'b'), (21, 1, 'b'), (22, 2, 'b'), (23, 3, 'a'), (24, 9, 'a'), (25, 2, 'b'), (26, 3, 'b'), (27, 2, 'a'), (28, 3, 'a'), (29, 5, 'b'), (30, 6, 'a'), (31, 9, 'b'), (32, 7, 'b'), (33, 8, 'b')])
db.commit()
PY
