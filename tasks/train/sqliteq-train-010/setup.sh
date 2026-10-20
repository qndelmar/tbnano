python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE samples (id INTEGER PRIMARY KEY, freq REAL)')
db.executescript('''
INSERT INTO samples (id, freq) VALUES (1, 102.9);
INSERT INTO samples (id, freq) VALUES (2, 156.7);
INSERT INTO samples (id, freq) VALUES (3, 6.2);
INSERT INTO samples (id, freq) VALUES (4, 126.3);
INSERT INTO samples (id, freq) VALUES (5, 108.4);
INSERT INTO samples (id, freq) VALUES (6, 180.2);
INSERT INTO samples (id, freq) VALUES (7, 132.6);
INSERT INTO samples (id, freq) VALUES (8, 59.4);
INSERT INTO samples (id, freq) VALUES (9, 63.8);
INSERT INTO samples (id, freq) VALUES (10, 153.5);
INSERT INTO samples (id, freq) VALUES (11, 63.1);
INSERT INTO samples (id, freq) VALUES (12, 31.7);
INSERT INTO samples (id, freq) VALUES (13, 68.4);
INSERT INTO samples (id, freq) VALUES (14, 85.5);
INSERT INTO samples (id, freq) VALUES (15, 141.8);
INSERT INTO samples (id, freq) VALUES (16, 52.7);
INSERT INTO samples (id, freq) VALUES (17, 132.6);
INSERT INTO samples (id, freq) VALUES (18, 125.4);
INSERT INTO samples (id, freq) VALUES (19, 161.4);
INSERT INTO samples (id, freq) VALUES (20, 116.4);
INSERT INTO samples (id, freq) VALUES (21, 146.8);
INSERT INTO samples (id, freq) VALUES (22, 126.2);
INSERT INTO samples (id, freq) VALUES (23, 193.6);
INSERT INTO samples (id, freq) VALUES (24, 77.7);
INSERT INTO samples (id, freq) VALUES (25, 81.7);
INSERT INTO samples (id, freq) VALUES (26, 37.2);
INSERT INTO samples (id, freq) VALUES (27, 194.6);
INSERT INTO samples (id, freq) VALUES (28, 177.7);
INSERT INTO samples (id, freq) VALUES (29, 97.8);
INSERT INTO samples (id, freq) VALUES (30, 120.8);
INSERT INTO samples (id, freq) VALUES (31, 109.2);
INSERT INTO samples (id, freq) VALUES (32, 132.5);
INSERT INTO samples (id, freq) VALUES (33, 106.4);
INSERT INTO samples (id, freq) VALUES (34, 61.4);
INSERT INTO samples (id, freq) VALUES (35, 46.8);
INSERT INTO samples (id, freq) VALUES (36, 163.5);
INSERT INTO samples (id, freq) VALUES (37, 78.7);
INSERT INTO samples (id, freq) VALUES (38, 70.7);
INSERT INTO samples (id, freq) VALUES (39, 158.1);
INSERT INTO samples (id, freq) VALUES (40, 184.8);
INSERT INTO samples (id, freq) VALUES (41, 154.2);
INSERT INTO samples (id, freq) VALUES (42, 143.3);
INSERT INTO samples (id, freq) VALUES (43, 122.9);
INSERT INTO samples (id, freq) VALUES (44, 145.3);
INSERT INTO samples (id, freq) VALUES (45, 54.5);
INSERT INTO samples (id, freq) VALUES (46, 22.4);
INSERT INTO samples (id, freq) VALUES (47, 80.1);
INSERT INTO samples (id, freq) VALUES (48, 86.8);
INSERT INTO samples (id, freq) VALUES (49, 164.7);
INSERT INTO samples (id, freq) VALUES (50, 136.3);
INSERT INTO samples (id, freq) VALUES (51, 184.7);
INSERT INTO samples (id, freq) VALUES (52, 10.7);
INSERT INTO samples (id, freq) VALUES (53, 81.8);
INSERT INTO samples (id, freq) VALUES (54, 35.8);
INSERT INTO samples (id, freq) VALUES (55, 129.8);
INSERT INTO samples (id, freq) VALUES (56, 126.4);
INSERT INTO samples (id, freq) VALUES (57, 61.6);
INSERT INTO samples (id, freq) VALUES (58, 46.1);
INSERT INTO samples (id, freq) VALUES (59, 123.3);
INSERT INTO samples (id, freq) VALUES (60, 198.4);
INSERT INTO samples (id, freq) VALUES (61, 116.2);
INSERT INTO samples (id, freq) VALUES (62, 187.1);
''')
db.commit(); db.close()
PY
