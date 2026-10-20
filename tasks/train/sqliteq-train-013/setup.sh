python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE channels (id INTEGER PRIMARY KEY, torque REAL)')
db.executescript('''
INSERT INTO channels (id, torque) VALUES (1, 127.7);
INSERT INTO channels (id, torque) VALUES (2, 110.9);
INSERT INTO channels (id, torque) VALUES (3, 21.1);
INSERT INTO channels (id, torque) VALUES (4, 100.1);
INSERT INTO channels (id, torque) VALUES (5, 151.0);
INSERT INTO channels (id, torque) VALUES (6, 109.8);
INSERT INTO channels (id, torque) VALUES (7, 23.0);
INSERT INTO channels (id, torque) VALUES (8, 98.5);
INSERT INTO channels (id, torque) VALUES (9, 94.4);
INSERT INTO channels (id, torque) VALUES (10, 26.2);
INSERT INTO channels (id, torque) VALUES (11, 45.0);
INSERT INTO channels (id, torque) VALUES (12, 60.6);
INSERT INTO channels (id, torque) VALUES (13, 90.7);
INSERT INTO channels (id, torque) VALUES (14, 11.4);
INSERT INTO channels (id, torque) VALUES (15, 36.2);
INSERT INTO channels (id, torque) VALUES (16, 195.0);
INSERT INTO channels (id, torque) VALUES (17, 52.8);
INSERT INTO channels (id, torque) VALUES (18, 110.9);
INSERT INTO channels (id, torque) VALUES (19, 89.2);
INSERT INTO channels (id, torque) VALUES (20, 119.1);
INSERT INTO channels (id, torque) VALUES (21, 2.9);
INSERT INTO channels (id, torque) VALUES (22, 98.9);
INSERT INTO channels (id, torque) VALUES (23, 61.5);
INSERT INTO channels (id, torque) VALUES (24, 16.6);
INSERT INTO channels (id, torque) VALUES (25, 134.9);
INSERT INTO channels (id, torque) VALUES (26, 18.3);
INSERT INTO channels (id, torque) VALUES (27, 145.4);
INSERT INTO channels (id, torque) VALUES (28, 155.2);
INSERT INTO channels (id, torque) VALUES (29, 185.2);
INSERT INTO channels (id, torque) VALUES (30, 73.2);
INSERT INTO channels (id, torque) VALUES (31, 76.3);
INSERT INTO channels (id, torque) VALUES (32, 173.3);
INSERT INTO channels (id, torque) VALUES (33, 62.2);
INSERT INTO channels (id, torque) VALUES (34, 48.3);
INSERT INTO channels (id, torque) VALUES (35, 24.8);
INSERT INTO channels (id, torque) VALUES (36, 14.7);
INSERT INTO channels (id, torque) VALUES (37, 63.9);
INSERT INTO channels (id, torque) VALUES (38, 132.4);
INSERT INTO channels (id, torque) VALUES (39, 160.7);
INSERT INTO channels (id, torque) VALUES (40, 187.7);
INSERT INTO channels (id, torque) VALUES (41, 16.6);
INSERT INTO channels (id, torque) VALUES (42, 72.2);
INSERT INTO channels (id, torque) VALUES (43, 7.4);
INSERT INTO channels (id, torque) VALUES (44, 4.7);
INSERT INTO channels (id, torque) VALUES (45, 72.6);
INSERT INTO channels (id, torque) VALUES (46, 192.5);
INSERT INTO channels (id, torque) VALUES (47, 33.7);
INSERT INTO channels (id, torque) VALUES (48, 104.1);
INSERT INTO channels (id, torque) VALUES (49, 30.4);
INSERT INTO channels (id, torque) VALUES (50, 63.8);
INSERT INTO channels (id, torque) VALUES (51, 139.7);
INSERT INTO channels (id, torque) VALUES (52, 147.7);
INSERT INTO channels (id, torque) VALUES (53, 20.9);
INSERT INTO channels (id, torque) VALUES (54, 133.2);
INSERT INTO channels (id, torque) VALUES (55, 58.8);
INSERT INTO channels (id, torque) VALUES (56, 152.0);
INSERT INTO channels (id, torque) VALUES (57, 109.4);
INSERT INTO channels (id, torque) VALUES (58, 30.2);
INSERT INTO channels (id, torque) VALUES (59, 14.0);
INSERT INTO channels (id, torque) VALUES (60, 101.3);
INSERT INTO channels (id, torque) VALUES (61, 54.6);
INSERT INTO channels (id, torque) VALUES (62, 168.8);
INSERT INTO channels (id, torque) VALUES (63, 106.6);
INSERT INTO channels (id, torque) VALUES (64, 143.5);
INSERT INTO channels (id, torque) VALUES (65, 92.0);
INSERT INTO channels (id, torque) VALUES (66, 179.0);
INSERT INTO channels (id, torque) VALUES (67, 62.6);
INSERT INTO channels (id, torque) VALUES (68, 156.3);
INSERT INTO channels (id, torque) VALUES (69, 137.4);
INSERT INTO channels (id, torque) VALUES (70, 173.4);
INSERT INTO channels (id, torque) VALUES (71, 3.8);
INSERT INTO channels (id, torque) VALUES (72, 98.1);
INSERT INTO channels (id, torque) VALUES (73, 21.9);
INSERT INTO channels (id, torque) VALUES (74, 36.9);
INSERT INTO channels (id, torque) VALUES (75, 137.0);
''')
db.commit(); db.close()
PY
