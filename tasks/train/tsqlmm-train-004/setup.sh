python3 - <<'PY'
import sqlite3
db = sqlite3.connect('m.db')
db.execute('CREATE TABLE t(id INTEGER, v INTEGER)')
db.executemany('INSERT INTO t VALUES(?,?)', [(0, 18), (1, 870), (2, 342), (3, 463), (4, 243), (5, 210), (6, 138), (7, 833), (8, 659), (9, 437), (10, 829), (11, 294), (12, 945), (13, 341), (14, 955), (15, 904), (16, 414), (17, 537), (18, 328), (19, 297), (20, 542), (21, 239), (22, 193), (23, 140), (24, 596)])
db.commit()
PY
