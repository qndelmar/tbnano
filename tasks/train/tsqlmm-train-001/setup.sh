python3 - <<'PY'
import sqlite3
db = sqlite3.connect('m.db')
db.execute('CREATE TABLE t(id INTEGER, v INTEGER)')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 545), (1, 842), (2, 952), (3, 273), (4, 706), (5, 152), (6, 309), (7, 126), (8, 700), (9, 410), (10, 601), (11, 317), (12, 464), (13, 324), (14, 798), (15, 762), (16, 486), (17, 140), (18, 779), (19, 67)])
db.commit()
PY
