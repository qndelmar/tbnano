python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE channels (id INTEGER PRIMARY KEY, torque REAL)')
db.executescript('''
INSERT INTO channels (id, torque) VALUES (1, 62.3);
INSERT INTO channels (id, torque) VALUES (2, 85.5);
INSERT INTO channels (id, torque) VALUES (3, 106.9);
INSERT INTO channels (id, torque) VALUES (4, 123.4);
INSERT INTO channels (id, torque) VALUES (5, 165.3);
INSERT INTO channels (id, torque) VALUES (6, 25.3);
INSERT INTO channels (id, torque) VALUES (7, 159.1);
INSERT INTO channels (id, torque) VALUES (8, 182.9);
INSERT INTO channels (id, torque) VALUES (9, 53.4);
INSERT INTO channels (id, torque) VALUES (10, 4.0);
INSERT INTO channels (id, torque) VALUES (11, 88.6);
INSERT INTO channels (id, torque) VALUES (12, 144.5);
INSERT INTO channels (id, torque) VALUES (13, 17.6);
INSERT INTO channels (id, torque) VALUES (14, 167.1);
INSERT INTO channels (id, torque) VALUES (15, 89.9);
INSERT INTO channels (id, torque) VALUES (16, 144.2);
INSERT INTO channels (id, torque) VALUES (17, 93.0);
INSERT INTO channels (id, torque) VALUES (18, 36.9);
INSERT INTO channels (id, torque) VALUES (19, 106.4);
INSERT INTO channels (id, torque) VALUES (20, 196.1);
INSERT INTO channels (id, torque) VALUES (21, 169.2);
INSERT INTO channels (id, torque) VALUES (22, 160.8);
INSERT INTO channels (id, torque) VALUES (23, 105.4);
INSERT INTO channels (id, torque) VALUES (24, 7.5);
INSERT INTO channels (id, torque) VALUES (25, 87.1);
INSERT INTO channels (id, torque) VALUES (26, 110.7);
INSERT INTO channels (id, torque) VALUES (27, 30.8);
INSERT INTO channels (id, torque) VALUES (28, 107.8);
INSERT INTO channels (id, torque) VALUES (29, 26.8);
INSERT INTO channels (id, torque) VALUES (30, 104.7);
INSERT INTO channels (id, torque) VALUES (31, 198.2);
INSERT INTO channels (id, torque) VALUES (32, 0.4);
INSERT INTO channels (id, torque) VALUES (33, 18.7);
INSERT INTO channels (id, torque) VALUES (34, 112.6);
INSERT INTO channels (id, torque) VALUES (35, 91.9);
INSERT INTO channels (id, torque) VALUES (36, 185.3);
INSERT INTO channels (id, torque) VALUES (37, 150.4);
INSERT INTO channels (id, torque) VALUES (38, 2.0);
INSERT INTO channels (id, torque) VALUES (39, 123.1);
INSERT INTO channels (id, torque) VALUES (40, 127.3);
INSERT INTO channels (id, torque) VALUES (41, 177.3);
INSERT INTO channels (id, torque) VALUES (42, 35.6);
INSERT INTO channels (id, torque) VALUES (43, 48.9);
INSERT INTO channels (id, torque) VALUES (44, 177.6);
INSERT INTO channels (id, torque) VALUES (45, 105.6);
INSERT INTO channels (id, torque) VALUES (46, 174.1);
INSERT INTO channels (id, torque) VALUES (47, 15.0);
INSERT INTO channels (id, torque) VALUES (48, 73.1);
INSERT INTO channels (id, torque) VALUES (49, 47.2);
INSERT INTO channels (id, torque) VALUES (50, 119.8);
INSERT INTO channels (id, torque) VALUES (51, 136.2);
INSERT INTO channels (id, torque) VALUES (52, 102.3);
INSERT INTO channels (id, torque) VALUES (53, 1.3);
INSERT INTO channels (id, torque) VALUES (54, 63.3);
INSERT INTO channels (id, torque) VALUES (55, 21.2);
INSERT INTO channels (id, torque) VALUES (56, 172.7);
INSERT INTO channels (id, torque) VALUES (57, 149.5);
INSERT INTO channels (id, torque) VALUES (58, 149.7);
INSERT INTO channels (id, torque) VALUES (59, 189.6);
INSERT INTO channels (id, torque) VALUES (60, 128.8);
INSERT INTO channels (id, torque) VALUES (61, 69.9);
INSERT INTO channels (id, torque) VALUES (62, 189.8);
INSERT INTO channels (id, torque) VALUES (63, 21.4);
INSERT INTO channels (id, torque) VALUES (64, 34.0);
INSERT INTO channels (id, torque) VALUES (65, 25.2);
INSERT INTO channels (id, torque) VALUES (66, 61.6);
INSERT INTO channels (id, torque) VALUES (67, 2.0);
INSERT INTO channels (id, torque) VALUES (68, 70.4);
INSERT INTO channels (id, torque) VALUES (69, 35.6);
INSERT INTO channels (id, torque) VALUES (70, 194.6);
INSERT INTO channels (id, torque) VALUES (71, 34.9);
INSERT INTO channels (id, torque) VALUES (72, 97.4);
INSERT INTO channels (id, torque) VALUES (73, 96.9);
INSERT INTO channels (id, torque) VALUES (74, 165.8);
INSERT INTO channels (id, torque) VALUES (75, 97.8);
INSERT INTO channels (id, torque) VALUES (76, 160.6);
INSERT INTO channels (id, torque) VALUES (77, 136.8);
INSERT INTO channels (id, torque) VALUES (78, 29.1);
''')
db.commit(); db.close()
PY
