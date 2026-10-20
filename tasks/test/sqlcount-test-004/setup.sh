python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER, g TEXT);')
db.executemany('INSERT INTO t VALUES(?,?,?)', [(0, 3, 'a'), (1, 8, 'b'), (2, 1, 'a'), (3, 4, 'b'), (4, 5, 'a'), (5, 3, 'a'), (6, 2, 'b'), (7, 6, 'a'), (8, 6, 'a'), (9, 9, 'b'), (10, 4, 'b'), (11, 3, 'b'), (12, 8, 'b'), (13, 4, 'a'), (14, 9, 'a'), (15, 6, 'b'), (16, 6, 'b'), (17, 5, 'a'), (18, 8, 'a'), (19, 7, 'a'), (20, 6, 'a'), (21, 7, 'a')])
db.commit()
PY
