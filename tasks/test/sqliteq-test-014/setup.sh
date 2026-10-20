python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE readings (id INTEGER PRIMARY KEY, rpm REAL)')
db.executescript('''
INSERT INTO readings (id, rpm) VALUES (1, 182.2);
INSERT INTO readings (id, rpm) VALUES (2, 107.8);
INSERT INTO readings (id, rpm) VALUES (3, 194.3);
INSERT INTO readings (id, rpm) VALUES (4, 43.7);
INSERT INTO readings (id, rpm) VALUES (5, 28.4);
INSERT INTO readings (id, rpm) VALUES (6, 66.5);
INSERT INTO readings (id, rpm) VALUES (7, 13.1);
INSERT INTO readings (id, rpm) VALUES (8, 41.6);
INSERT INTO readings (id, rpm) VALUES (9, 74.7);
INSERT INTO readings (id, rpm) VALUES (10, 53.6);
INSERT INTO readings (id, rpm) VALUES (11, 120.0);
INSERT INTO readings (id, rpm) VALUES (12, 11.6);
INSERT INTO readings (id, rpm) VALUES (13, 14.7);
INSERT INTO readings (id, rpm) VALUES (14, 105.7);
INSERT INTO readings (id, rpm) VALUES (15, 91.8);
INSERT INTO readings (id, rpm) VALUES (16, 73.1);
INSERT INTO readings (id, rpm) VALUES (17, 27.1);
INSERT INTO readings (id, rpm) VALUES (18, 125.0);
INSERT INTO readings (id, rpm) VALUES (19, 87.5);
INSERT INTO readings (id, rpm) VALUES (20, 92.1);
INSERT INTO readings (id, rpm) VALUES (21, 74.3);
INSERT INTO readings (id, rpm) VALUES (22, 186.5);
INSERT INTO readings (id, rpm) VALUES (23, 94.2);
INSERT INTO readings (id, rpm) VALUES (24, 143.3);
INSERT INTO readings (id, rpm) VALUES (25, 158.3);
INSERT INTO readings (id, rpm) VALUES (26, 165.7);
INSERT INTO readings (id, rpm) VALUES (27, 116.1);
INSERT INTO readings (id, rpm) VALUES (28, 173.8);
INSERT INTO readings (id, rpm) VALUES (29, 196.4);
INSERT INTO readings (id, rpm) VALUES (30, 187.5);
INSERT INTO readings (id, rpm) VALUES (31, 99.4);
INSERT INTO readings (id, rpm) VALUES (32, 163.2);
INSERT INTO readings (id, rpm) VALUES (33, 195.0);
INSERT INTO readings (id, rpm) VALUES (34, 94.6);
INSERT INTO readings (id, rpm) VALUES (35, 85.0);
INSERT INTO readings (id, rpm) VALUES (36, 51.7);
INSERT INTO readings (id, rpm) VALUES (37, 11.6);
INSERT INTO readings (id, rpm) VALUES (38, 177.3);
INSERT INTO readings (id, rpm) VALUES (39, 185.5);
INSERT INTO readings (id, rpm) VALUES (40, 62.7);
INSERT INTO readings (id, rpm) VALUES (41, 162.8);
INSERT INTO readings (id, rpm) VALUES (42, 166.5);
INSERT INTO readings (id, rpm) VALUES (43, 110.3);
INSERT INTO readings (id, rpm) VALUES (44, 83.1);
INSERT INTO readings (id, rpm) VALUES (45, 101.5);
INSERT INTO readings (id, rpm) VALUES (46, 3.0);
INSERT INTO readings (id, rpm) VALUES (47, 45.9);
INSERT INTO readings (id, rpm) VALUES (48, 86.3);
INSERT INTO readings (id, rpm) VALUES (49, 75.5);
INSERT INTO readings (id, rpm) VALUES (50, 66.6);
INSERT INTO readings (id, rpm) VALUES (51, 114.1);
INSERT INTO readings (id, rpm) VALUES (52, 88.2);
INSERT INTO readings (id, rpm) VALUES (53, 178.2);
INSERT INTO readings (id, rpm) VALUES (54, 124.1);
INSERT INTO readings (id, rpm) VALUES (55, 191.4);
INSERT INTO readings (id, rpm) VALUES (56, 181.9);
INSERT INTO readings (id, rpm) VALUES (57, 83.4);
INSERT INTO readings (id, rpm) VALUES (58, 138.7);
INSERT INTO readings (id, rpm) VALUES (59, 125.1);
INSERT INTO readings (id, rpm) VALUES (60, 124.4);
INSERT INTO readings (id, rpm) VALUES (61, 183.9);
INSERT INTO readings (id, rpm) VALUES (62, 72.8);
INSERT INTO readings (id, rpm) VALUES (63, 36.6);
INSERT INTO readings (id, rpm) VALUES (64, 41.9);
INSERT INTO readings (id, rpm) VALUES (65, 93.7);
INSERT INTO readings (id, rpm) VALUES (66, 153.3);
INSERT INTO readings (id, rpm) VALUES (67, 13.6);
INSERT INTO readings (id, rpm) VALUES (68, 162.8);
INSERT INTO readings (id, rpm) VALUES (69, 91.6);
INSERT INTO readings (id, rpm) VALUES (70, 38.7);
INSERT INTO readings (id, rpm) VALUES (71, 79.3);
INSERT INTO readings (id, rpm) VALUES (72, 109.1);
INSERT INTO readings (id, rpm) VALUES (73, 135.2);
INSERT INTO readings (id, rpm) VALUES (74, 116.9);
''')
db.commit(); db.close()
PY
