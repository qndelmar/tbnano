python3 - <<'PY'
import sqlite3
db = sqlite3.connect('m.db')
db.execute('CREATE TABLE t(id INTEGER, v INTEGER)')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 291), (1, 207), (2, 936), (3, 802), (4, 140), (5, 238), (6, 480), (7, 607), (8, 37), (9, 437), (10, 820), (11, 874), (12, 3), (13, 676), (14, 337), (15, 809)])
db.commit()
PY
