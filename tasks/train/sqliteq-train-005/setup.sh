python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE channels (id INTEGER PRIMARY KEY, torque REAL)')
db.executescript('''
INSERT INTO channels (id, torque) VALUES (1, 45.1);
INSERT INTO channels (id, torque) VALUES (2, 67.4);
INSERT INTO channels (id, torque) VALUES (3, 75.5);
INSERT INTO channels (id, torque) VALUES (4, 26.9);
INSERT INTO channels (id, torque) VALUES (5, 55.2);
INSERT INTO channels (id, torque) VALUES (6, 46.4);
INSERT INTO channels (id, torque) VALUES (7, 197.7);
INSERT INTO channels (id, torque) VALUES (8, 157.6);
INSERT INTO channels (id, torque) VALUES (9, 80.1);
INSERT INTO channels (id, torque) VALUES (10, 126.8);
INSERT INTO channels (id, torque) VALUES (11, 128.9);
INSERT INTO channels (id, torque) VALUES (12, 111.4);
INSERT INTO channels (id, torque) VALUES (13, 125.0);
INSERT INTO channels (id, torque) VALUES (14, 196.9);
INSERT INTO channels (id, torque) VALUES (15, 65.7);
INSERT INTO channels (id, torque) VALUES (16, 79.3);
INSERT INTO channels (id, torque) VALUES (17, 96.3);
INSERT INTO channels (id, torque) VALUES (18, 58.7);
INSERT INTO channels (id, torque) VALUES (19, 80.0);
INSERT INTO channels (id, torque) VALUES (20, 175.0);
INSERT INTO channels (id, torque) VALUES (21, 115.9);
INSERT INTO channels (id, torque) VALUES (22, 155.3);
INSERT INTO channels (id, torque) VALUES (23, 89.4);
INSERT INTO channels (id, torque) VALUES (24, 159.6);
INSERT INTO channels (id, torque) VALUES (25, 142.2);
INSERT INTO channels (id, torque) VALUES (26, 145.6);
INSERT INTO channels (id, torque) VALUES (27, 141.6);
INSERT INTO channels (id, torque) VALUES (28, 16.9);
INSERT INTO channels (id, torque) VALUES (29, 44.9);
INSERT INTO channels (id, torque) VALUES (30, 46.6);
INSERT INTO channels (id, torque) VALUES (31, 183.2);
INSERT INTO channels (id, torque) VALUES (32, 70.0);
INSERT INTO channels (id, torque) VALUES (33, 2.7);
INSERT INTO channels (id, torque) VALUES (34, 102.9);
INSERT INTO channels (id, torque) VALUES (35, 87.6);
INSERT INTO channels (id, torque) VALUES (36, 154.9);
INSERT INTO channels (id, torque) VALUES (37, 92.0);
INSERT INTO channels (id, torque) VALUES (38, 29.6);
INSERT INTO channels (id, torque) VALUES (39, 90.2);
''')
db.commit(); db.close()
PY
