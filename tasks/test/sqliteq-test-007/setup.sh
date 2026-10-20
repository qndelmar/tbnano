python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE readings (id INTEGER PRIMARY KEY, rpm REAL)')
db.executescript('''
INSERT INTO readings (id, rpm) VALUES (1, 89.5);
INSERT INTO readings (id, rpm) VALUES (2, 16.1);
INSERT INTO readings (id, rpm) VALUES (3, 149.6);
INSERT INTO readings (id, rpm) VALUES (4, 55.4);
INSERT INTO readings (id, rpm) VALUES (5, 45.0);
INSERT INTO readings (id, rpm) VALUES (6, 165.3);
INSERT INTO readings (id, rpm) VALUES (7, 31.3);
INSERT INTO readings (id, rpm) VALUES (8, 111.6);
INSERT INTO readings (id, rpm) VALUES (9, 46.0);
INSERT INTO readings (id, rpm) VALUES (10, 138.8);
INSERT INTO readings (id, rpm) VALUES (11, 62.7);
INSERT INTO readings (id, rpm) VALUES (12, 86.3);
INSERT INTO readings (id, rpm) VALUES (13, 7.5);
INSERT INTO readings (id, rpm) VALUES (14, 58.8);
INSERT INTO readings (id, rpm) VALUES (15, 88.8);
INSERT INTO readings (id, rpm) VALUES (16, 92.5);
INSERT INTO readings (id, rpm) VALUES (17, 93.8);
INSERT INTO readings (id, rpm) VALUES (18, 43.0);
INSERT INTO readings (id, rpm) VALUES (19, 95.4);
INSERT INTO readings (id, rpm) VALUES (20, 26.4);
INSERT INTO readings (id, rpm) VALUES (21, 97.3);
INSERT INTO readings (id, rpm) VALUES (22, 147.1);
INSERT INTO readings (id, rpm) VALUES (23, 58.8);
INSERT INTO readings (id, rpm) VALUES (24, 22.2);
INSERT INTO readings (id, rpm) VALUES (25, 55.9);
INSERT INTO readings (id, rpm) VALUES (26, 90.5);
INSERT INTO readings (id, rpm) VALUES (27, 120.9);
INSERT INTO readings (id, rpm) VALUES (28, 152.3);
INSERT INTO readings (id, rpm) VALUES (29, 25.6);
INSERT INTO readings (id, rpm) VALUES (30, 193.6);
INSERT INTO readings (id, rpm) VALUES (31, 83.7);
INSERT INTO readings (id, rpm) VALUES (32, 40.1);
INSERT INTO readings (id, rpm) VALUES (33, 50.7);
INSERT INTO readings (id, rpm) VALUES (34, 64.9);
INSERT INTO readings (id, rpm) VALUES (35, 113.4);
INSERT INTO readings (id, rpm) VALUES (36, 47.6);
INSERT INTO readings (id, rpm) VALUES (37, 188.7);
INSERT INTO readings (id, rpm) VALUES (38, 28.9);
INSERT INTO readings (id, rpm) VALUES (39, 183.5);
INSERT INTO readings (id, rpm) VALUES (40, 11.7);
INSERT INTO readings (id, rpm) VALUES (41, 63.2);
INSERT INTO readings (id, rpm) VALUES (42, 136.0);
''')
db.commit(); db.close()
PY
