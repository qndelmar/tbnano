python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE channels (id INTEGER PRIMARY KEY, current REAL)')
db.executescript('''
INSERT INTO channels (id, current) VALUES (1, 9.6);
INSERT INTO channels (id, current) VALUES (2, 25.5);
INSERT INTO channels (id, current) VALUES (3, 18.5);
INSERT INTO channels (id, current) VALUES (4, 22.0);
INSERT INTO channels (id, current) VALUES (5, 132.0);
INSERT INTO channels (id, current) VALUES (6, 161.7);
INSERT INTO channels (id, current) VALUES (7, 152.6);
INSERT INTO channels (id, current) VALUES (8, 189.5);
INSERT INTO channels (id, current) VALUES (9, 158.7);
INSERT INTO channels (id, current) VALUES (10, 111.9);
INSERT INTO channels (id, current) VALUES (11, 58.2);
INSERT INTO channels (id, current) VALUES (12, 144.1);
INSERT INTO channels (id, current) VALUES (13, 24.5);
INSERT INTO channels (id, current) VALUES (14, 68.9);
INSERT INTO channels (id, current) VALUES (15, 85.4);
INSERT INTO channels (id, current) VALUES (16, 148.8);
INSERT INTO channels (id, current) VALUES (17, 25.0);
INSERT INTO channels (id, current) VALUES (18, 133.1);
INSERT INTO channels (id, current) VALUES (19, 19.6);
INSERT INTO channels (id, current) VALUES (20, 61.2);
INSERT INTO channels (id, current) VALUES (21, 8.0);
INSERT INTO channels (id, current) VALUES (22, 165.1);
INSERT INTO channels (id, current) VALUES (23, 0.4);
INSERT INTO channels (id, current) VALUES (24, 26.3);
INSERT INTO channels (id, current) VALUES (25, 0.9);
INSERT INTO channels (id, current) VALUES (26, 3.8);
INSERT INTO channels (id, current) VALUES (27, 164.3);
INSERT INTO channels (id, current) VALUES (28, 3.1);
INSERT INTO channels (id, current) VALUES (29, 149.7);
INSERT INTO channels (id, current) VALUES (30, 127.4);
INSERT INTO channels (id, current) VALUES (31, 104.7);
INSERT INTO channels (id, current) VALUES (32, 135.1);
INSERT INTO channels (id, current) VALUES (33, 84.1);
''')
db.commit(); db.close()
PY
