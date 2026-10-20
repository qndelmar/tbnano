python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE telemetry (id INTEGER PRIMARY KEY, temp REAL)')
db.executescript('''
INSERT INTO telemetry (id, temp) VALUES (1, 95.9);
INSERT INTO telemetry (id, temp) VALUES (2, 54.7);
INSERT INTO telemetry (id, temp) VALUES (3, 187.6);
INSERT INTO telemetry (id, temp) VALUES (4, 127.1);
INSERT INTO telemetry (id, temp) VALUES (5, 30.2);
INSERT INTO telemetry (id, temp) VALUES (6, 117.4);
INSERT INTO telemetry (id, temp) VALUES (7, 20.2);
INSERT INTO telemetry (id, temp) VALUES (8, 78.4);
INSERT INTO telemetry (id, temp) VALUES (9, 171.1);
INSERT INTO telemetry (id, temp) VALUES (10, 67.3);
INSERT INTO telemetry (id, temp) VALUES (11, 129.7);
INSERT INTO telemetry (id, temp) VALUES (12, 11.2);
INSERT INTO telemetry (id, temp) VALUES (13, 139.2);
INSERT INTO telemetry (id, temp) VALUES (14, 119.1);
INSERT INTO telemetry (id, temp) VALUES (15, 11.9);
INSERT INTO telemetry (id, temp) VALUES (16, 171.1);
INSERT INTO telemetry (id, temp) VALUES (17, 90.9);
INSERT INTO telemetry (id, temp) VALUES (18, 21.5);
INSERT INTO telemetry (id, temp) VALUES (19, 150.6);
INSERT INTO telemetry (id, temp) VALUES (20, 192.9);
INSERT INTO telemetry (id, temp) VALUES (21, 102.3);
INSERT INTO telemetry (id, temp) VALUES (22, 71.7);
INSERT INTO telemetry (id, temp) VALUES (23, 61.7);
INSERT INTO telemetry (id, temp) VALUES (24, 41.5);
INSERT INTO telemetry (id, temp) VALUES (25, 28.8);
INSERT INTO telemetry (id, temp) VALUES (26, 92.8);
INSERT INTO telemetry (id, temp) VALUES (27, 104.7);
INSERT INTO telemetry (id, temp) VALUES (28, 100.5);
INSERT INTO telemetry (id, temp) VALUES (29, 163.4);
INSERT INTO telemetry (id, temp) VALUES (30, 12.4);
INSERT INTO telemetry (id, temp) VALUES (31, 158.7);
INSERT INTO telemetry (id, temp) VALUES (32, 133.1);
INSERT INTO telemetry (id, temp) VALUES (33, 73.9);
INSERT INTO telemetry (id, temp) VALUES (34, 38.1);
INSERT INTO telemetry (id, temp) VALUES (35, 189.5);
INSERT INTO telemetry (id, temp) VALUES (36, 95.5);
INSERT INTO telemetry (id, temp) VALUES (37, 89.3);
''')
db.commit(); db.close()
PY
