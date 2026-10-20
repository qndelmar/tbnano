python3 - <<'PY'
import sqlite3
db = sqlite3.connect('m.db')
db.execute('CREATE TABLE t(id INTEGER, v INTEGER)')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 219), (1, 914), (2, 354), (3, 149), (4, 972), (5, 845), (6, 266), (7, 849), (8, 136), (9, 366), (10, 749), (11, 498), (12, 538), (13, 56), (14, 115), (15, 817), (16, 25), (17, 373), (18, 5), (19, 461), (20, 655), (21, 977), (22, 682), (23, 468), (24, 989), (25, 89), (26, 398)])
db.commit()
PY
