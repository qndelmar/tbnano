python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE readings (id INTEGER PRIMARY KEY, voltage REAL)')
db.executescript('''
INSERT INTO readings (id, voltage) VALUES (1, 13.5);
INSERT INTO readings (id, voltage) VALUES (2, 59.4);
INSERT INTO readings (id, voltage) VALUES (3, 140.9);
INSERT INTO readings (id, voltage) VALUES (4, 45.7);
INSERT INTO readings (id, voltage) VALUES (5, 80.2);
INSERT INTO readings (id, voltage) VALUES (6, 191.0);
INSERT INTO readings (id, voltage) VALUES (7, 64.6);
INSERT INTO readings (id, voltage) VALUES (8, 31.2);
INSERT INTO readings (id, voltage) VALUES (9, 85.9);
INSERT INTO readings (id, voltage) VALUES (10, 13.1);
INSERT INTO readings (id, voltage) VALUES (11, 65.7);
INSERT INTO readings (id, voltage) VALUES (12, 196.8);
INSERT INTO readings (id, voltage) VALUES (13, 137.6);
INSERT INTO readings (id, voltage) VALUES (14, 174.0);
INSERT INTO readings (id, voltage) VALUES (15, 91.4);
INSERT INTO readings (id, voltage) VALUES (16, 120.7);
INSERT INTO readings (id, voltage) VALUES (17, 158.5);
INSERT INTO readings (id, voltage) VALUES (18, 75.0);
INSERT INTO readings (id, voltage) VALUES (19, 114.1);
INSERT INTO readings (id, voltage) VALUES (20, 51.8);
INSERT INTO readings (id, voltage) VALUES (21, 11.7);
INSERT INTO readings (id, voltage) VALUES (22, 99.1);
INSERT INTO readings (id, voltage) VALUES (23, 119.3);
INSERT INTO readings (id, voltage) VALUES (24, 67.0);
INSERT INTO readings (id, voltage) VALUES (25, 41.1);
INSERT INTO readings (id, voltage) VALUES (26, 63.2);
INSERT INTO readings (id, voltage) VALUES (27, 65.6);
INSERT INTO readings (id, voltage) VALUES (28, 169.9);
INSERT INTO readings (id, voltage) VALUES (29, 77.0);
INSERT INTO readings (id, voltage) VALUES (30, 103.7);
INSERT INTO readings (id, voltage) VALUES (31, 157.1);
INSERT INTO readings (id, voltage) VALUES (32, 107.3);
INSERT INTO readings (id, voltage) VALUES (33, 157.7);
INSERT INTO readings (id, voltage) VALUES (34, 109.6);
INSERT INTO readings (id, voltage) VALUES (35, 29.2);
INSERT INTO readings (id, voltage) VALUES (36, 92.2);
INSERT INTO readings (id, voltage) VALUES (37, 146.3);
INSERT INTO readings (id, voltage) VALUES (38, 175.2);
INSERT INTO readings (id, voltage) VALUES (39, 112.4);
INSERT INTO readings (id, voltage) VALUES (40, 1.8);
INSERT INTO readings (id, voltage) VALUES (41, 35.6);
INSERT INTO readings (id, voltage) VALUES (42, 135.9);
INSERT INTO readings (id, voltage) VALUES (43, 133.0);
INSERT INTO readings (id, voltage) VALUES (44, 41.9);
INSERT INTO readings (id, voltage) VALUES (45, 26.0);
INSERT INTO readings (id, voltage) VALUES (46, 198.4);
INSERT INTO readings (id, voltage) VALUES (47, 3.4);
INSERT INTO readings (id, voltage) VALUES (48, 90.0);
INSERT INTO readings (id, voltage) VALUES (49, 90.5);
INSERT INTO readings (id, voltage) VALUES (50, 179.6);
INSERT INTO readings (id, voltage) VALUES (51, 15.6);
INSERT INTO readings (id, voltage) VALUES (52, 53.5);
INSERT INTO readings (id, voltage) VALUES (53, 190.7);
INSERT INTO readings (id, voltage) VALUES (54, 32.0);
INSERT INTO readings (id, voltage) VALUES (55, 172.0);
INSERT INTO readings (id, voltage) VALUES (56, 24.7);
INSERT INTO readings (id, voltage) VALUES (57, 28.9);
INSERT INTO readings (id, voltage) VALUES (58, 110.7);
INSERT INTO readings (id, voltage) VALUES (59, 110.2);
INSERT INTO readings (id, voltage) VALUES (60, 188.0);
INSERT INTO readings (id, voltage) VALUES (61, 149.9);
INSERT INTO readings (id, voltage) VALUES (62, 107.3);
INSERT INTO readings (id, voltage) VALUES (63, 69.7);
INSERT INTO readings (id, voltage) VALUES (64, 1.8);
INSERT INTO readings (id, voltage) VALUES (65, 171.1);
INSERT INTO readings (id, voltage) VALUES (66, 19.2);
INSERT INTO readings (id, voltage) VALUES (67, 179.2);
INSERT INTO readings (id, voltage) VALUES (68, 190.0);
INSERT INTO readings (id, voltage) VALUES (69, 42.6);
INSERT INTO readings (id, voltage) VALUES (70, 78.0);
INSERT INTO readings (id, voltage) VALUES (71, 103.8);
''')
db.commit(); db.close()
PY
