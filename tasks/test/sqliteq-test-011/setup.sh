python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE readings (id INTEGER PRIMARY KEY, temp REAL)')
db.executescript('''
INSERT INTO readings (id, temp) VALUES (1, 141.9);
INSERT INTO readings (id, temp) VALUES (2, 145.0);
INSERT INTO readings (id, temp) VALUES (3, 19.6);
INSERT INTO readings (id, temp) VALUES (4, 31.7);
INSERT INTO readings (id, temp) VALUES (5, 23.0);
INSERT INTO readings (id, temp) VALUES (6, 171.3);
INSERT INTO readings (id, temp) VALUES (7, 42.0);
INSERT INTO readings (id, temp) VALUES (8, 118.4);
INSERT INTO readings (id, temp) VALUES (9, 6.4);
INSERT INTO readings (id, temp) VALUES (10, 22.9);
INSERT INTO readings (id, temp) VALUES (11, 116.7);
INSERT INTO readings (id, temp) VALUES (12, 100.7);
INSERT INTO readings (id, temp) VALUES (13, 26.8);
INSERT INTO readings (id, temp) VALUES (14, 188.8);
INSERT INTO readings (id, temp) VALUES (15, 164.7);
INSERT INTO readings (id, temp) VALUES (16, 191.3);
INSERT INTO readings (id, temp) VALUES (17, 107.4);
INSERT INTO readings (id, temp) VALUES (18, 25.4);
INSERT INTO readings (id, temp) VALUES (19, 28.9);
INSERT INTO readings (id, temp) VALUES (20, 45.3);
INSERT INTO readings (id, temp) VALUES (21, 77.8);
INSERT INTO readings (id, temp) VALUES (22, 101.7);
INSERT INTO readings (id, temp) VALUES (23, 26.5);
INSERT INTO readings (id, temp) VALUES (24, 62.1);
INSERT INTO readings (id, temp) VALUES (25, 92.1);
INSERT INTO readings (id, temp) VALUES (26, 162.1);
INSERT INTO readings (id, temp) VALUES (27, 55.5);
INSERT INTO readings (id, temp) VALUES (28, 145.4);
INSERT INTO readings (id, temp) VALUES (29, 12.2);
INSERT INTO readings (id, temp) VALUES (30, 51.8);
''')
db.commit(); db.close()
PY
