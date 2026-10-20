python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE samples (id INTEGER PRIMARY KEY, current REAL)')
db.executescript('''
INSERT INTO samples (id, current) VALUES (1, 185.9);
INSERT INTO samples (id, current) VALUES (2, 124.6);
INSERT INTO samples (id, current) VALUES (3, 122.0);
INSERT INTO samples (id, current) VALUES (4, 128.9);
INSERT INTO samples (id, current) VALUES (5, 168.5);
INSERT INTO samples (id, current) VALUES (6, 150.4);
INSERT INTO samples (id, current) VALUES (7, 50.2);
INSERT INTO samples (id, current) VALUES (8, 45.3);
INSERT INTO samples (id, current) VALUES (9, 90.3);
INSERT INTO samples (id, current) VALUES (10, 162.8);
INSERT INTO samples (id, current) VALUES (11, 94.1);
INSERT INTO samples (id, current) VALUES (12, 148.9);
INSERT INTO samples (id, current) VALUES (13, 25.3);
INSERT INTO samples (id, current) VALUES (14, 64.6);
INSERT INTO samples (id, current) VALUES (15, 112.9);
INSERT INTO samples (id, current) VALUES (16, 176.0);
INSERT INTO samples (id, current) VALUES (17, 172.8);
INSERT INTO samples (id, current) VALUES (18, 147.6);
INSERT INTO samples (id, current) VALUES (19, 182.3);
INSERT INTO samples (id, current) VALUES (20, 139.4);
INSERT INTO samples (id, current) VALUES (21, 96.7);
INSERT INTO samples (id, current) VALUES (22, 96.3);
INSERT INTO samples (id, current) VALUES (23, 171.2);
INSERT INTO samples (id, current) VALUES (24, 194.1);
INSERT INTO samples (id, current) VALUES (25, 170.4);
INSERT INTO samples (id, current) VALUES (26, 58.8);
INSERT INTO samples (id, current) VALUES (27, 44.1);
INSERT INTO samples (id, current) VALUES (28, 116.0);
INSERT INTO samples (id, current) VALUES (29, 20.3);
INSERT INTO samples (id, current) VALUES (30, 193.8);
INSERT INTO samples (id, current) VALUES (31, 152.9);
INSERT INTO samples (id, current) VALUES (32, 187.5);
INSERT INTO samples (id, current) VALUES (33, 155.2);
''')
db.commit(); db.close()
PY
