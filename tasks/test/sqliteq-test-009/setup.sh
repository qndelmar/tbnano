python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE telemetry (id INTEGER PRIMARY KEY, rpm REAL)')
db.executescript('''
INSERT INTO telemetry (id, rpm) VALUES (1, 36.2);
INSERT INTO telemetry (id, rpm) VALUES (2, 105.1);
INSERT INTO telemetry (id, rpm) VALUES (3, 49.6);
INSERT INTO telemetry (id, rpm) VALUES (4, 134.2);
INSERT INTO telemetry (id, rpm) VALUES (5, 142.4);
INSERT INTO telemetry (id, rpm) VALUES (6, 130.6);
INSERT INTO telemetry (id, rpm) VALUES (7, 123.4);
INSERT INTO telemetry (id, rpm) VALUES (8, 169.2);
INSERT INTO telemetry (id, rpm) VALUES (9, 128.8);
INSERT INTO telemetry (id, rpm) VALUES (10, 161.6);
INSERT INTO telemetry (id, rpm) VALUES (11, 164.5);
INSERT INTO telemetry (id, rpm) VALUES (12, 130.9);
INSERT INTO telemetry (id, rpm) VALUES (13, 129.9);
INSERT INTO telemetry (id, rpm) VALUES (14, 52.7);
INSERT INTO telemetry (id, rpm) VALUES (15, 2.1);
INSERT INTO telemetry (id, rpm) VALUES (16, 9.6);
INSERT INTO telemetry (id, rpm) VALUES (17, 190.5);
INSERT INTO telemetry (id, rpm) VALUES (18, 17.8);
INSERT INTO telemetry (id, rpm) VALUES (19, 175.1);
INSERT INTO telemetry (id, rpm) VALUES (20, 69.1);
INSERT INTO telemetry (id, rpm) VALUES (21, 182.7);
INSERT INTO telemetry (id, rpm) VALUES (22, 118.0);
INSERT INTO telemetry (id, rpm) VALUES (23, 18.4);
INSERT INTO telemetry (id, rpm) VALUES (24, 133.5);
INSERT INTO telemetry (id, rpm) VALUES (25, 47.4);
INSERT INTO telemetry (id, rpm) VALUES (26, 132.5);
INSERT INTO telemetry (id, rpm) VALUES (27, 31.5);
INSERT INTO telemetry (id, rpm) VALUES (28, 88.6);
INSERT INTO telemetry (id, rpm) VALUES (29, 148.1);
INSERT INTO telemetry (id, rpm) VALUES (30, 130.8);
INSERT INTO telemetry (id, rpm) VALUES (31, 125.1);
INSERT INTO telemetry (id, rpm) VALUES (32, 15.5);
INSERT INTO telemetry (id, rpm) VALUES (33, 170.4);
INSERT INTO telemetry (id, rpm) VALUES (34, 33.1);
INSERT INTO telemetry (id, rpm) VALUES (35, 96.3);
INSERT INTO telemetry (id, rpm) VALUES (36, 182.8);
INSERT INTO telemetry (id, rpm) VALUES (37, 20.1);
INSERT INTO telemetry (id, rpm) VALUES (38, 33.3);
INSERT INTO telemetry (id, rpm) VALUES (39, 187.7);
INSERT INTO telemetry (id, rpm) VALUES (40, 132.4);
INSERT INTO telemetry (id, rpm) VALUES (41, 158.5);
INSERT INTO telemetry (id, rpm) VALUES (42, 106.3);
''')
db.commit(); db.close()
PY
