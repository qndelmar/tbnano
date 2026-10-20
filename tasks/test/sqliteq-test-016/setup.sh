python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE events (id INTEGER PRIMARY KEY, temp REAL)')
db.executescript('''
INSERT INTO events (id, temp) VALUES (1, 38.2);
INSERT INTO events (id, temp) VALUES (2, 34.9);
INSERT INTO events (id, temp) VALUES (3, 30.1);
INSERT INTO events (id, temp) VALUES (4, 16.6);
INSERT INTO events (id, temp) VALUES (5, 47.1);
INSERT INTO events (id, temp) VALUES (6, 111.0);
INSERT INTO events (id, temp) VALUES (7, 149.1);
INSERT INTO events (id, temp) VALUES (8, 170.1);
INSERT INTO events (id, temp) VALUES (9, 147.6);
INSERT INTO events (id, temp) VALUES (10, 153.7);
INSERT INTO events (id, temp) VALUES (11, 161.8);
INSERT INTO events (id, temp) VALUES (12, 94.6);
INSERT INTO events (id, temp) VALUES (13, 181.9);
INSERT INTO events (id, temp) VALUES (14, 173.1);
INSERT INTO events (id, temp) VALUES (15, 157.7);
INSERT INTO events (id, temp) VALUES (16, 196.3);
INSERT INTO events (id, temp) VALUES (17, 130.4);
INSERT INTO events (id, temp) VALUES (18, 19.8);
INSERT INTO events (id, temp) VALUES (19, 122.8);
INSERT INTO events (id, temp) VALUES (20, 57.4);
INSERT INTO events (id, temp) VALUES (21, 32.5);
INSERT INTO events (id, temp) VALUES (22, 90.1);
INSERT INTO events (id, temp) VALUES (23, 31.0);
INSERT INTO events (id, temp) VALUES (24, 189.7);
INSERT INTO events (id, temp) VALUES (25, 175.3);
INSERT INTO events (id, temp) VALUES (26, 79.5);
INSERT INTO events (id, temp) VALUES (27, 198.7);
INSERT INTO events (id, temp) VALUES (28, 7.5);
INSERT INTO events (id, temp) VALUES (29, 92.3);
INSERT INTO events (id, temp) VALUES (30, 110.2);
INSERT INTO events (id, temp) VALUES (31, 28.3);
INSERT INTO events (id, temp) VALUES (32, 95.8);
INSERT INTO events (id, temp) VALUES (33, 159.2);
INSERT INTO events (id, temp) VALUES (34, 180.0);
INSERT INTO events (id, temp) VALUES (35, 11.0);
''')
db.commit(); db.close()
PY
