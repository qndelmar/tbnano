python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE readings (id INTEGER PRIMARY KEY, voltage REAL)')
db.executescript('''
INSERT INTO readings (id, voltage) VALUES (1, 117.6);
INSERT INTO readings (id, voltage) VALUES (2, 96.7);
INSERT INTO readings (id, voltage) VALUES (3, 17.9);
INSERT INTO readings (id, voltage) VALUES (4, 140.8);
INSERT INTO readings (id, voltage) VALUES (5, 167.3);
INSERT INTO readings (id, voltage) VALUES (6, 129.9);
INSERT INTO readings (id, voltage) VALUES (7, 31.0);
INSERT INTO readings (id, voltage) VALUES (8, 198.0);
INSERT INTO readings (id, voltage) VALUES (9, 43.4);
INSERT INTO readings (id, voltage) VALUES (10, 28.5);
INSERT INTO readings (id, voltage) VALUES (11, 142.6);
INSERT INTO readings (id, voltage) VALUES (12, 194.5);
INSERT INTO readings (id, voltage) VALUES (13, 105.2);
INSERT INTO readings (id, voltage) VALUES (14, 103.2);
INSERT INTO readings (id, voltage) VALUES (15, 95.7);
INSERT INTO readings (id, voltage) VALUES (16, 15.0);
INSERT INTO readings (id, voltage) VALUES (17, 4.8);
INSERT INTO readings (id, voltage) VALUES (18, 193.2);
INSERT INTO readings (id, voltage) VALUES (19, 165.9);
INSERT INTO readings (id, voltage) VALUES (20, 11.9);
INSERT INTO readings (id, voltage) VALUES (21, 56.6);
INSERT INTO readings (id, voltage) VALUES (22, 199.8);
INSERT INTO readings (id, voltage) VALUES (23, 48.4);
INSERT INTO readings (id, voltage) VALUES (24, 88.4);
INSERT INTO readings (id, voltage) VALUES (25, 135.6);
INSERT INTO readings (id, voltage) VALUES (26, 11.0);
INSERT INTO readings (id, voltage) VALUES (27, 26.6);
INSERT INTO readings (id, voltage) VALUES (28, 177.7);
INSERT INTO readings (id, voltage) VALUES (29, 47.6);
INSERT INTO readings (id, voltage) VALUES (30, 110.7);
INSERT INTO readings (id, voltage) VALUES (31, 32.7);
INSERT INTO readings (id, voltage) VALUES (32, 102.2);
INSERT INTO readings (id, voltage) VALUES (33, 10.3);
INSERT INTO readings (id, voltage) VALUES (34, 62.3);
INSERT INTO readings (id, voltage) VALUES (35, 27.7);
INSERT INTO readings (id, voltage) VALUES (36, 118.2);
INSERT INTO readings (id, voltage) VALUES (37, 162.1);
INSERT INTO readings (id, voltage) VALUES (38, 169.8);
INSERT INTO readings (id, voltage) VALUES (39, 2.5);
INSERT INTO readings (id, voltage) VALUES (40, 49.7);
INSERT INTO readings (id, voltage) VALUES (41, 77.2);
INSERT INTO readings (id, voltage) VALUES (42, 115.6);
INSERT INTO readings (id, voltage) VALUES (43, 178.5);
INSERT INTO readings (id, voltage) VALUES (44, 85.6);
INSERT INTO readings (id, voltage) VALUES (45, 6.6);
INSERT INTO readings (id, voltage) VALUES (46, 130.1);
INSERT INTO readings (id, voltage) VALUES (47, 196.6);
INSERT INTO readings (id, voltage) VALUES (48, 82.1);
INSERT INTO readings (id, voltage) VALUES (49, 87.9);
INSERT INTO readings (id, voltage) VALUES (50, 165.2);
INSERT INTO readings (id, voltage) VALUES (51, 73.7);
INSERT INTO readings (id, voltage) VALUES (52, 167.8);
INSERT INTO readings (id, voltage) VALUES (53, 108.0);
INSERT INTO readings (id, voltage) VALUES (54, 134.9);
INSERT INTO readings (id, voltage) VALUES (55, 40.2);
INSERT INTO readings (id, voltage) VALUES (56, 120.2);
INSERT INTO readings (id, voltage) VALUES (57, 27.0);
INSERT INTO readings (id, voltage) VALUES (58, 37.5);
INSERT INTO readings (id, voltage) VALUES (59, 25.5);
INSERT INTO readings (id, voltage) VALUES (60, 69.2);
INSERT INTO readings (id, voltage) VALUES (61, 151.2);
INSERT INTO readings (id, voltage) VALUES (62, 172.1);
INSERT INTO readings (id, voltage) VALUES (63, 32.5);
INSERT INTO readings (id, voltage) VALUES (64, 31.3);
INSERT INTO readings (id, voltage) VALUES (65, 183.6);
INSERT INTO readings (id, voltage) VALUES (66, 149.3);
INSERT INTO readings (id, voltage) VALUES (67, 136.3);
INSERT INTO readings (id, voltage) VALUES (68, 105.0);
INSERT INTO readings (id, voltage) VALUES (69, 152.3);
INSERT INTO readings (id, voltage) VALUES (70, 97.5);
INSERT INTO readings (id, voltage) VALUES (71, 74.0);
INSERT INTO readings (id, voltage) VALUES (72, 190.1);
INSERT INTO readings (id, voltage) VALUES (73, 61.8);
INSERT INTO readings (id, voltage) VALUES (74, 37.9);
INSERT INTO readings (id, voltage) VALUES (75, 124.4);
INSERT INTO readings (id, voltage) VALUES (76, 176.0);
INSERT INTO readings (id, voltage) VALUES (77, 21.9);
INSERT INTO readings (id, voltage) VALUES (78, 187.0);
''')
db.commit(); db.close()
PY
