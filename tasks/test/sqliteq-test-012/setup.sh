python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE events (id INTEGER PRIMARY KEY, pressure REAL)')
db.executescript('''
INSERT INTO events (id, pressure) VALUES (1, 74.9);
INSERT INTO events (id, pressure) VALUES (2, 21.1);
INSERT INTO events (id, pressure) VALUES (3, 19.4);
INSERT INTO events (id, pressure) VALUES (4, 19.2);
INSERT INTO events (id, pressure) VALUES (5, 151.3);
INSERT INTO events (id, pressure) VALUES (6, 197.5);
INSERT INTO events (id, pressure) VALUES (7, 63.0);
INSERT INTO events (id, pressure) VALUES (8, 178.7);
INSERT INTO events (id, pressure) VALUES (9, 194.4);
INSERT INTO events (id, pressure) VALUES (10, 55.9);
INSERT INTO events (id, pressure) VALUES (11, 191.6);
INSERT INTO events (id, pressure) VALUES (12, 101.0);
INSERT INTO events (id, pressure) VALUES (13, 48.8);
INSERT INTO events (id, pressure) VALUES (14, 48.3);
INSERT INTO events (id, pressure) VALUES (15, 135.6);
INSERT INTO events (id, pressure) VALUES (16, 49.5);
INSERT INTO events (id, pressure) VALUES (17, 86.4);
INSERT INTO events (id, pressure) VALUES (18, 121.7);
INSERT INTO events (id, pressure) VALUES (19, 60.0);
INSERT INTO events (id, pressure) VALUES (20, 130.2);
INSERT INTO events (id, pressure) VALUES (21, 4.1);
INSERT INTO events (id, pressure) VALUES (22, 191.4);
INSERT INTO events (id, pressure) VALUES (23, 83.8);
INSERT INTO events (id, pressure) VALUES (24, 182.3);
INSERT INTO events (id, pressure) VALUES (25, 53.6);
INSERT INTO events (id, pressure) VALUES (26, 168.0);
INSERT INTO events (id, pressure) VALUES (27, 70.1);
INSERT INTO events (id, pressure) VALUES (28, 76.4);
INSERT INTO events (id, pressure) VALUES (29, 145.7);
INSERT INTO events (id, pressure) VALUES (30, 48.7);
INSERT INTO events (id, pressure) VALUES (31, 104.5);
INSERT INTO events (id, pressure) VALUES (32, 49.9);
INSERT INTO events (id, pressure) VALUES (33, 79.1);
INSERT INTO events (id, pressure) VALUES (34, 44.4);
INSERT INTO events (id, pressure) VALUES (35, 184.6);
INSERT INTO events (id, pressure) VALUES (36, 103.1);
INSERT INTO events (id, pressure) VALUES (37, 31.2);
INSERT INTO events (id, pressure) VALUES (38, 98.5);
INSERT INTO events (id, pressure) VALUES (39, 175.0);
INSERT INTO events (id, pressure) VALUES (40, 73.5);
INSERT INTO events (id, pressure) VALUES (41, 160.0);
INSERT INTO events (id, pressure) VALUES (42, 114.0);
INSERT INTO events (id, pressure) VALUES (43, 99.3);
INSERT INTO events (id, pressure) VALUES (44, 145.7);
INSERT INTO events (id, pressure) VALUES (45, 189.2);
INSERT INTO events (id, pressure) VALUES (46, 147.4);
INSERT INTO events (id, pressure) VALUES (47, 162.4);
INSERT INTO events (id, pressure) VALUES (48, 79.2);
INSERT INTO events (id, pressure) VALUES (49, 91.0);
INSERT INTO events (id, pressure) VALUES (50, 159.8);
INSERT INTO events (id, pressure) VALUES (51, 165.5);
INSERT INTO events (id, pressure) VALUES (52, 100.3);
INSERT INTO events (id, pressure) VALUES (53, 37.5);
INSERT INTO events (id, pressure) VALUES (54, 89.8);
''')
db.commit(); db.close()
PY
