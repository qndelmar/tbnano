python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE measures (id INTEGER PRIMARY KEY, freq REAL)')
db.executescript('''
INSERT INTO measures (id, freq) VALUES (1, 69.4);
INSERT INTO measures (id, freq) VALUES (2, 144.7);
INSERT INTO measures (id, freq) VALUES (3, 146.6);
INSERT INTO measures (id, freq) VALUES (4, 85.9);
INSERT INTO measures (id, freq) VALUES (5, 141.8);
INSERT INTO measures (id, freq) VALUES (6, 32.8);
INSERT INTO measures (id, freq) VALUES (7, 161.7);
INSERT INTO measures (id, freq) VALUES (8, 175.0);
INSERT INTO measures (id, freq) VALUES (9, 147.8);
INSERT INTO measures (id, freq) VALUES (10, 69.6);
INSERT INTO measures (id, freq) VALUES (11, 52.4);
INSERT INTO measures (id, freq) VALUES (12, 91.1);
INSERT INTO measures (id, freq) VALUES (13, 52.0);
INSERT INTO measures (id, freq) VALUES (14, 179.5);
INSERT INTO measures (id, freq) VALUES (15, 47.8);
INSERT INTO measures (id, freq) VALUES (16, 20.3);
INSERT INTO measures (id, freq) VALUES (17, 82.1);
INSERT INTO measures (id, freq) VALUES (18, 100.5);
INSERT INTO measures (id, freq) VALUES (19, 127.6);
INSERT INTO measures (id, freq) VALUES (20, 71.9);
INSERT INTO measures (id, freq) VALUES (21, 161.2);
INSERT INTO measures (id, freq) VALUES (22, 127.0);
INSERT INTO measures (id, freq) VALUES (23, 164.3);
INSERT INTO measures (id, freq) VALUES (24, 117.9);
INSERT INTO measures (id, freq) VALUES (25, 46.2);
INSERT INTO measures (id, freq) VALUES (26, 145.5);
INSERT INTO measures (id, freq) VALUES (27, 28.3);
INSERT INTO measures (id, freq) VALUES (28, 190.5);
INSERT INTO measures (id, freq) VALUES (29, 161.4);
INSERT INTO measures (id, freq) VALUES (30, 76.9);
INSERT INTO measures (id, freq) VALUES (31, 105.0);
INSERT INTO measures (id, freq) VALUES (32, 42.3);
INSERT INTO measures (id, freq) VALUES (33, 3.3);
INSERT INTO measures (id, freq) VALUES (34, 25.3);
INSERT INTO measures (id, freq) VALUES (35, 4.1);
INSERT INTO measures (id, freq) VALUES (36, 125.1);
INSERT INTO measures (id, freq) VALUES (37, 40.3);
INSERT INTO measures (id, freq) VALUES (38, 112.3);
INSERT INTO measures (id, freq) VALUES (39, 79.1);
INSERT INTO measures (id, freq) VALUES (40, 114.1);
INSERT INTO measures (id, freq) VALUES (41, 115.8);
INSERT INTO measures (id, freq) VALUES (42, 97.8);
INSERT INTO measures (id, freq) VALUES (43, 31.4);
INSERT INTO measures (id, freq) VALUES (44, 175.5);
INSERT INTO measures (id, freq) VALUES (45, 24.2);
INSERT INTO measures (id, freq) VALUES (46, 131.0);
INSERT INTO measures (id, freq) VALUES (47, 123.8);
INSERT INTO measures (id, freq) VALUES (48, 1.2);
INSERT INTO measures (id, freq) VALUES (49, 118.0);
INSERT INTO measures (id, freq) VALUES (50, 69.6);
INSERT INTO measures (id, freq) VALUES (51, 101.7);
INSERT INTO measures (id, freq) VALUES (52, 60.1);
INSERT INTO measures (id, freq) VALUES (53, 135.1);
INSERT INTO measures (id, freq) VALUES (54, 73.9);
INSERT INTO measures (id, freq) VALUES (55, 4.0);
INSERT INTO measures (id, freq) VALUES (56, 96.4);
INSERT INTO measures (id, freq) VALUES (57, 142.2);
INSERT INTO measures (id, freq) VALUES (58, 127.7);
INSERT INTO measures (id, freq) VALUES (59, 169.5);
INSERT INTO measures (id, freq) VALUES (60, 112.5);
INSERT INTO measures (id, freq) VALUES (61, 53.3);
INSERT INTO measures (id, freq) VALUES (62, 60.9);
INSERT INTO measures (id, freq) VALUES (63, 16.4);
INSERT INTO measures (id, freq) VALUES (64, 56.4);
INSERT INTO measures (id, freq) VALUES (65, 21.1);
INSERT INTO measures (id, freq) VALUES (66, 197.4);
INSERT INTO measures (id, freq) VALUES (67, 193.9);
''')
db.commit(); db.close()
PY
