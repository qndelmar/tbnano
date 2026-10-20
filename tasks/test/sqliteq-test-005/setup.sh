python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE readings (id INTEGER PRIMARY KEY, voltage REAL)')
db.executescript('''
INSERT INTO readings (id, voltage) VALUES (1, 89.0);
INSERT INTO readings (id, voltage) VALUES (2, 146.3);
INSERT INTO readings (id, voltage) VALUES (3, 180.5);
INSERT INTO readings (id, voltage) VALUES (4, 146.5);
INSERT INTO readings (id, voltage) VALUES (5, 175.9);
INSERT INTO readings (id, voltage) VALUES (6, 25.1);
INSERT INTO readings (id, voltage) VALUES (7, 11.0);
INSERT INTO readings (id, voltage) VALUES (8, 148.4);
INSERT INTO readings (id, voltage) VALUES (9, 145.2);
INSERT INTO readings (id, voltage) VALUES (10, 17.1);
INSERT INTO readings (id, voltage) VALUES (11, 157.8);
INSERT INTO readings (id, voltage) VALUES (12, 160.0);
INSERT INTO readings (id, voltage) VALUES (13, 88.2);
INSERT INTO readings (id, voltage) VALUES (14, 91.5);
INSERT INTO readings (id, voltage) VALUES (15, 182.0);
INSERT INTO readings (id, voltage) VALUES (16, 12.1);
INSERT INTO readings (id, voltage) VALUES (17, 162.0);
INSERT INTO readings (id, voltage) VALUES (18, 143.1);
INSERT INTO readings (id, voltage) VALUES (19, 19.8);
INSERT INTO readings (id, voltage) VALUES (20, 126.0);
INSERT INTO readings (id, voltage) VALUES (21, 116.9);
INSERT INTO readings (id, voltage) VALUES (22, 39.1);
INSERT INTO readings (id, voltage) VALUES (23, 71.9);
INSERT INTO readings (id, voltage) VALUES (24, 177.5);
INSERT INTO readings (id, voltage) VALUES (25, 196.4);
INSERT INTO readings (id, voltage) VALUES (26, 41.8);
INSERT INTO readings (id, voltage) VALUES (27, 141.6);
INSERT INTO readings (id, voltage) VALUES (28, 152.2);
INSERT INTO readings (id, voltage) VALUES (29, 14.1);
INSERT INTO readings (id, voltage) VALUES (30, 45.0);
INSERT INTO readings (id, voltage) VALUES (31, 135.6);
INSERT INTO readings (id, voltage) VALUES (32, 122.1);
INSERT INTO readings (id, voltage) VALUES (33, 151.0);
INSERT INTO readings (id, voltage) VALUES (34, 109.5);
INSERT INTO readings (id, voltage) VALUES (35, 131.9);
INSERT INTO readings (id, voltage) VALUES (36, 99.3);
INSERT INTO readings (id, voltage) VALUES (37, 85.4);
INSERT INTO readings (id, voltage) VALUES (38, 9.3);
INSERT INTO readings (id, voltage) VALUES (39, 124.3);
INSERT INTO readings (id, voltage) VALUES (40, 107.0);
INSERT INTO readings (id, voltage) VALUES (41, 157.2);
INSERT INTO readings (id, voltage) VALUES (42, 71.5);
INSERT INTO readings (id, voltage) VALUES (43, 38.6);
INSERT INTO readings (id, voltage) VALUES (44, 185.6);
INSERT INTO readings (id, voltage) VALUES (45, 15.4);
INSERT INTO readings (id, voltage) VALUES (46, 80.2);
INSERT INTO readings (id, voltage) VALUES (47, 53.2);
INSERT INTO readings (id, voltage) VALUES (48, 20.2);
INSERT INTO readings (id, voltage) VALUES (49, 103.7);
INSERT INTO readings (id, voltage) VALUES (50, 166.4);
INSERT INTO readings (id, voltage) VALUES (51, 158.6);
INSERT INTO readings (id, voltage) VALUES (52, 47.7);
INSERT INTO readings (id, voltage) VALUES (53, 164.0);
INSERT INTO readings (id, voltage) VALUES (54, 77.0);
INSERT INTO readings (id, voltage) VALUES (55, 27.8);
INSERT INTO readings (id, voltage) VALUES (56, 150.1);
''')
db.commit(); db.close()
PY
