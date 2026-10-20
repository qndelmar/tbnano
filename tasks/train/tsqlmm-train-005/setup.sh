python3 - <<'PY'
import sqlite3
db = sqlite3.connect('m.db')
db.execute('CREATE TABLE t(id INTEGER, v INTEGER)')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 704), (1, 693), (2, 287), (3, 952), (4, 894), (5, 600), (6, 527), (7, 850), (8, 601), (9, 459), (10, 872), (11, 599), (12, 853), (13, 600), (14, 12), (15, 608), (16, 137), (17, 399), (18, 408), (19, 332), (20, 306), (21, 484), (22, 20), (23, 722)])
db.commit()
PY
