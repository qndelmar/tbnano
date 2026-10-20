python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE events (id INTEGER PRIMARY KEY, rpm REAL)')
db.executescript('''
INSERT INTO events (id, rpm) VALUES (1, 103.0);
INSERT INTO events (id, rpm) VALUES (2, 102.7);
INSERT INTO events (id, rpm) VALUES (3, 169.8);
INSERT INTO events (id, rpm) VALUES (4, 138.2);
INSERT INTO events (id, rpm) VALUES (5, 153.6);
INSERT INTO events (id, rpm) VALUES (6, 110.5);
INSERT INTO events (id, rpm) VALUES (7, 142.6);
INSERT INTO events (id, rpm) VALUES (8, 64.6);
INSERT INTO events (id, rpm) VALUES (9, 61.5);
INSERT INTO events (id, rpm) VALUES (10, 115.7);
INSERT INTO events (id, rpm) VALUES (11, 31.3);
INSERT INTO events (id, rpm) VALUES (12, 144.7);
INSERT INTO events (id, rpm) VALUES (13, 106.2);
INSERT INTO events (id, rpm) VALUES (14, 193.1);
INSERT INTO events (id, rpm) VALUES (15, 168.0);
INSERT INTO events (id, rpm) VALUES (16, 93.0);
INSERT INTO events (id, rpm) VALUES (17, 167.1);
INSERT INTO events (id, rpm) VALUES (18, 143.1);
INSERT INTO events (id, rpm) VALUES (19, 61.0);
INSERT INTO events (id, rpm) VALUES (20, 169.3);
INSERT INTO events (id, rpm) VALUES (21, 199.6);
INSERT INTO events (id, rpm) VALUES (22, 121.5);
INSERT INTO events (id, rpm) VALUES (23, 32.3);
INSERT INTO events (id, rpm) VALUES (24, 43.1);
INSERT INTO events (id, rpm) VALUES (25, 91.9);
INSERT INTO events (id, rpm) VALUES (26, 119.9);
INSERT INTO events (id, rpm) VALUES (27, 66.1);
INSERT INTO events (id, rpm) VALUES (28, 27.0);
INSERT INTO events (id, rpm) VALUES (29, 23.9);
INSERT INTO events (id, rpm) VALUES (30, 164.7);
''')
db.commit(); db.close()
PY
