python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE measures (id INTEGER PRIMARY KEY, freq REAL)')
db.executescript('''
INSERT INTO measures (id, freq) VALUES (1, 69.0);
INSERT INTO measures (id, freq) VALUES (2, 113.0);
INSERT INTO measures (id, freq) VALUES (3, 152.5);
INSERT INTO measures (id, freq) VALUES (4, 87.8);
INSERT INTO measures (id, freq) VALUES (5, 38.4);
INSERT INTO measures (id, freq) VALUES (6, 9.7);
INSERT INTO measures (id, freq) VALUES (7, 75.4);
INSERT INTO measures (id, freq) VALUES (8, 106.5);
INSERT INTO measures (id, freq) VALUES (9, 57.6);
INSERT INTO measures (id, freq) VALUES (10, 129.5);
INSERT INTO measures (id, freq) VALUES (11, 190.6);
INSERT INTO measures (id, freq) VALUES (12, 123.4);
INSERT INTO measures (id, freq) VALUES (13, 100.8);
INSERT INTO measures (id, freq) VALUES (14, 128.7);
INSERT INTO measures (id, freq) VALUES (15, 199.7);
INSERT INTO measures (id, freq) VALUES (16, 134.6);
INSERT INTO measures (id, freq) VALUES (17, 132.4);
INSERT INTO measures (id, freq) VALUES (18, 130.8);
INSERT INTO measures (id, freq) VALUES (19, 0.7);
INSERT INTO measures (id, freq) VALUES (20, 114.6);
INSERT INTO measures (id, freq) VALUES (21, 127.2);
INSERT INTO measures (id, freq) VALUES (22, 38.8);
INSERT INTO measures (id, freq) VALUES (23, 63.6);
INSERT INTO measures (id, freq) VALUES (24, 164.3);
INSERT INTO measures (id, freq) VALUES (25, 140.2);
INSERT INTO measures (id, freq) VALUES (26, 149.7);
INSERT INTO measures (id, freq) VALUES (27, 115.0);
INSERT INTO measures (id, freq) VALUES (28, 179.4);
INSERT INTO measures (id, freq) VALUES (29, 31.3);
INSERT INTO measures (id, freq) VALUES (30, 116.2);
INSERT INTO measures (id, freq) VALUES (31, 80.7);
INSERT INTO measures (id, freq) VALUES (32, 159.3);
INSERT INTO measures (id, freq) VALUES (33, 86.7);
INSERT INTO measures (id, freq) VALUES (34, 53.8);
INSERT INTO measures (id, freq) VALUES (35, 80.3);
INSERT INTO measures (id, freq) VALUES (36, 14.4);
INSERT INTO measures (id, freq) VALUES (37, 60.7);
INSERT INTO measures (id, freq) VALUES (38, 13.4);
INSERT INTO measures (id, freq) VALUES (39, 174.6);
INSERT INTO measures (id, freq) VALUES (40, 154.1);
INSERT INTO measures (id, freq) VALUES (41, 147.5);
INSERT INTO measures (id, freq) VALUES (42, 177.3);
INSERT INTO measures (id, freq) VALUES (43, 2.1);
INSERT INTO measures (id, freq) VALUES (44, 106.2);
INSERT INTO measures (id, freq) VALUES (45, 83.9);
INSERT INTO measures (id, freq) VALUES (46, 141.0);
INSERT INTO measures (id, freq) VALUES (47, 190.2);
INSERT INTO measures (id, freq) VALUES (48, 93.8);
INSERT INTO measures (id, freq) VALUES (49, 122.3);
INSERT INTO measures (id, freq) VALUES (50, 91.7);
INSERT INTO measures (id, freq) VALUES (51, 118.4);
INSERT INTO measures (id, freq) VALUES (52, 165.1);
INSERT INTO measures (id, freq) VALUES (53, 124.4);
INSERT INTO measures (id, freq) VALUES (54, 8.1);
INSERT INTO measures (id, freq) VALUES (55, 28.0);
INSERT INTO measures (id, freq) VALUES (56, 188.2);
INSERT INTO measures (id, freq) VALUES (57, 178.6);
INSERT INTO measures (id, freq) VALUES (58, 186.2);
INSERT INTO measures (id, freq) VALUES (59, 112.4);
INSERT INTO measures (id, freq) VALUES (60, 146.8);
INSERT INTO measures (id, freq) VALUES (61, 134.8);
INSERT INTO measures (id, freq) VALUES (62, 139.2);
INSERT INTO measures (id, freq) VALUES (63, 86.1);
INSERT INTO measures (id, freq) VALUES (64, 143.6);
INSERT INTO measures (id, freq) VALUES (65, 19.0);
INSERT INTO measures (id, freq) VALUES (66, 42.5);
INSERT INTO measures (id, freq) VALUES (67, 106.8);
INSERT INTO measures (id, freq) VALUES (68, 106.1);
INSERT INTO measures (id, freq) VALUES (69, 66.2);
INSERT INTO measures (id, freq) VALUES (70, 3.3);
INSERT INTO measures (id, freq) VALUES (71, 147.4);
''')
db.commit(); db.close()
PY
