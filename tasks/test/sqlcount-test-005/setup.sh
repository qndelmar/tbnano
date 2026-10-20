python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER, g TEXT);')
db.executemany('INSERT INTO t VALUES(?,?,?)', [(0, 7, 'a'), (1, 1, 'a'), (2, 6, 'b'), (3, 3, 'a'), (4, 3, 'b'), (5, 7, 'a'), (6, 5, 'b'), (7, 3, 'b'), (8, 1, 'b'), (9, 2, 'a'), (10, 9, 'b'), (11, 4, 'b'), (12, 9, 'a'), (13, 7, 'b'), (14, 6, 'b'), (15, 8, 'a'), (16, 6, 'b'), (17, 7, 'b'), (18, 9, 'a'), (19, 3, 'a'), (20, 2, 'b'), (21, 3, 'b'), (22, 7, 'a'), (23, 4, 'a'), (24, 6, 'b'), (25, 9, 'a'), (26, 2, 'b'), (27, 1, 'b'), (28, 7, 'a'), (29, 3, 'b'), (30, 2, 'a'), (31, 2, 'a'), (32, 6, 'b'), (33, 7, 'a'), (34, 6, 'a'), (35, 3, 'b'), (36, 1, 'a')])
db.commit()
PY
