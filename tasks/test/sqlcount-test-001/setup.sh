python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER, g TEXT);')
db.executemany('INSERT INTO t VALUES(?,?,?)', [(0, 2, 'a'), (1, 4, 'a'), (2, 3, 'b'), (3, 8, 'a'), (4, 5, 'b'), (5, 3, 'b'), (6, 2, 'b'), (7, 6, 'b'), (8, 2, 'a'), (9, 8, 'a'), (10, 1, 'b'), (11, 8, 'a'), (12, 2, 'a'), (13, 9, 'b'), (14, 4, 'b'), (15, 5, 'b'), (16, 6, 'a'), (17, 7, 'b'), (18, 5, 'a'), (19, 4, 'a'), (20, 8, 'b'), (21, 9, 'b'), (22, 5, 'b'), (23, 9, 'a'), (24, 6, 'a'), (25, 6, 'b'), (26, 1, 'a')])
db.commit()
PY
