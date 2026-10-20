python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE samples (id INTEGER PRIMARY KEY, flow REAL)')
db.executescript('''
INSERT INTO samples (id, flow) VALUES (1, 89.8);
INSERT INTO samples (id, flow) VALUES (2, 38.1);
INSERT INTO samples (id, flow) VALUES (3, 111.0);
INSERT INTO samples (id, flow) VALUES (4, 81.6);
INSERT INTO samples (id, flow) VALUES (5, 51.8);
INSERT INTO samples (id, flow) VALUES (6, 187.6);
INSERT INTO samples (id, flow) VALUES (7, 132.2);
INSERT INTO samples (id, flow) VALUES (8, 173.9);
INSERT INTO samples (id, flow) VALUES (9, 125.9);
INSERT INTO samples (id, flow) VALUES (10, 137.2);
INSERT INTO samples (id, flow) VALUES (11, 25.4);
INSERT INTO samples (id, flow) VALUES (12, 39.2);
INSERT INTO samples (id, flow) VALUES (13, 179.4);
INSERT INTO samples (id, flow) VALUES (14, 107.3);
INSERT INTO samples (id, flow) VALUES (15, 23.8);
INSERT INTO samples (id, flow) VALUES (16, 126.5);
INSERT INTO samples (id, flow) VALUES (17, 21.0);
INSERT INTO samples (id, flow) VALUES (18, 40.3);
INSERT INTO samples (id, flow) VALUES (19, 103.2);
INSERT INTO samples (id, flow) VALUES (20, 160.9);
INSERT INTO samples (id, flow) VALUES (21, 100.9);
INSERT INTO samples (id, flow) VALUES (22, 193.8);
INSERT INTO samples (id, flow) VALUES (23, 34.8);
INSERT INTO samples (id, flow) VALUES (24, 194.5);
INSERT INTO samples (id, flow) VALUES (25, 69.8);
INSERT INTO samples (id, flow) VALUES (26, 58.1);
INSERT INTO samples (id, flow) VALUES (27, 119.5);
INSERT INTO samples (id, flow) VALUES (28, 33.3);
INSERT INTO samples (id, flow) VALUES (29, 92.2);
INSERT INTO samples (id, flow) VALUES (30, 23.9);
INSERT INTO samples (id, flow) VALUES (31, 37.0);
''')
db.commit(); db.close()
PY
