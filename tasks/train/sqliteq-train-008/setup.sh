python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE samples (id INTEGER PRIMARY KEY, flow REAL)')
db.executescript('''
INSERT INTO samples (id, flow) VALUES (1, 34.3);
INSERT INTO samples (id, flow) VALUES (2, 5.5);
INSERT INTO samples (id, flow) VALUES (3, 114.0);
INSERT INTO samples (id, flow) VALUES (4, 43.9);
INSERT INTO samples (id, flow) VALUES (5, 43.9);
INSERT INTO samples (id, flow) VALUES (6, 20.9);
INSERT INTO samples (id, flow) VALUES (7, 18.3);
INSERT INTO samples (id, flow) VALUES (8, 18.5);
INSERT INTO samples (id, flow) VALUES (9, 64.5);
INSERT INTO samples (id, flow) VALUES (10, 193.7);
INSERT INTO samples (id, flow) VALUES (11, 98.2);
INSERT INTO samples (id, flow) VALUES (12, 34.4);
INSERT INTO samples (id, flow) VALUES (13, 152.4);
INSERT INTO samples (id, flow) VALUES (14, 51.7);
INSERT INTO samples (id, flow) VALUES (15, 88.0);
INSERT INTO samples (id, flow) VALUES (16, 48.0);
INSERT INTO samples (id, flow) VALUES (17, 151.9);
INSERT INTO samples (id, flow) VALUES (18, 83.1);
INSERT INTO samples (id, flow) VALUES (19, 67.2);
INSERT INTO samples (id, flow) VALUES (20, 198.1);
INSERT INTO samples (id, flow) VALUES (21, 159.7);
INSERT INTO samples (id, flow) VALUES (22, 108.3);
INSERT INTO samples (id, flow) VALUES (23, 13.3);
INSERT INTO samples (id, flow) VALUES (24, 160.5);
INSERT INTO samples (id, flow) VALUES (25, 197.3);
INSERT INTO samples (id, flow) VALUES (26, 165.1);
INSERT INTO samples (id, flow) VALUES (27, 130.7);
INSERT INTO samples (id, flow) VALUES (28, 142.4);
INSERT INTO samples (id, flow) VALUES (29, 28.0);
INSERT INTO samples (id, flow) VALUES (30, 43.7);
INSERT INTO samples (id, flow) VALUES (31, 37.7);
INSERT INTO samples (id, flow) VALUES (32, 91.9);
INSERT INTO samples (id, flow) VALUES (33, 180.7);
INSERT INTO samples (id, flow) VALUES (34, 7.0);
INSERT INTO samples (id, flow) VALUES (35, 0.9);
INSERT INTO samples (id, flow) VALUES (36, 162.4);
INSERT INTO samples (id, flow) VALUES (37, 23.3);
INSERT INTO samples (id, flow) VALUES (38, 169.5);
INSERT INTO samples (id, flow) VALUES (39, 50.3);
INSERT INTO samples (id, flow) VALUES (40, 32.8);
INSERT INTO samples (id, flow) VALUES (41, 186.0);
INSERT INTO samples (id, flow) VALUES (42, 111.3);
INSERT INTO samples (id, flow) VALUES (43, 154.1);
INSERT INTO samples (id, flow) VALUES (44, 198.1);
INSERT INTO samples (id, flow) VALUES (45, 44.9);
INSERT INTO samples (id, flow) VALUES (46, 154.0);
INSERT INTO samples (id, flow) VALUES (47, 9.0);
INSERT INTO samples (id, flow) VALUES (48, 128.8);
INSERT INTO samples (id, flow) VALUES (49, 87.6);
INSERT INTO samples (id, flow) VALUES (50, 184.8);
INSERT INTO samples (id, flow) VALUES (51, 115.5);
INSERT INTO samples (id, flow) VALUES (52, 150.1);
INSERT INTO samples (id, flow) VALUES (53, 25.9);
INSERT INTO samples (id, flow) VALUES (54, 165.2);
INSERT INTO samples (id, flow) VALUES (55, 135.5);
INSERT INTO samples (id, flow) VALUES (56, 1.1);
''')
db.commit(); db.close()
PY
