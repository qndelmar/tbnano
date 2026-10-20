python3 - <<'PY'
import sqlite3
db = sqlite3.connect('data.db')
db.executescript('CREATE TABLE t(id INTEGER PRIMARY KEY, v INTEGER, g TEXT);')
db.executemany('INSERT INTO t VALUES(?,?,?)', [(0, 7, 'b'), (1, 4, 'a'), (2, 7, 'b'), (3, 3, 'a'), (4, 7, 'b'), (5, 6, 'a'), (6, 6, 'a'), (7, 7, 'b'), (8, 7, 'b'), (9, 3, 'b'), (10, 6, 'a'), (11, 9, 'b'), (12, 8, 'b'), (13, 5, 'b'), (14, 3, 'b'), (15, 9, 'b'), (16, 2, 'b'), (17, 7, 'b'), (18, 2, 'b'), (19, 7, 'b')])
db.commit()
PY
