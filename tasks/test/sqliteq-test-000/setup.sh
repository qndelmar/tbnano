python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE telemetry (id INTEGER PRIMARY KEY, temp REAL)')
db.executescript('''
INSERT INTO telemetry (id, temp) VALUES (1, 87.4);
INSERT INTO telemetry (id, temp) VALUES (2, 28.0);
INSERT INTO telemetry (id, temp) VALUES (3, 85.1);
INSERT INTO telemetry (id, temp) VALUES (4, 104.2);
INSERT INTO telemetry (id, temp) VALUES (5, 88.8);
INSERT INTO telemetry (id, temp) VALUES (6, 165.1);
INSERT INTO telemetry (id, temp) VALUES (7, 97.9);
INSERT INTO telemetry (id, temp) VALUES (8, 112.4);
INSERT INTO telemetry (id, temp) VALUES (9, 83.5);
INSERT INTO telemetry (id, temp) VALUES (10, 147.3);
INSERT INTO telemetry (id, temp) VALUES (11, 88.9);
INSERT INTO telemetry (id, temp) VALUES (12, 136.1);
INSERT INTO telemetry (id, temp) VALUES (13, 0.4);
INSERT INTO telemetry (id, temp) VALUES (14, 184.5);
INSERT INTO telemetry (id, temp) VALUES (15, 113.1);
INSERT INTO telemetry (id, temp) VALUES (16, 0.0);
INSERT INTO telemetry (id, temp) VALUES (17, 58.4);
INSERT INTO telemetry (id, temp) VALUES (18, 48.3);
INSERT INTO telemetry (id, temp) VALUES (19, 161.4);
INSERT INTO telemetry (id, temp) VALUES (20, 77.0);
INSERT INTO telemetry (id, temp) VALUES (21, 109.6);
INSERT INTO telemetry (id, temp) VALUES (22, 99.4);
INSERT INTO telemetry (id, temp) VALUES (23, 67.5);
INSERT INTO telemetry (id, temp) VALUES (24, 72.7);
INSERT INTO telemetry (id, temp) VALUES (25, 170.0);
INSERT INTO telemetry (id, temp) VALUES (26, 102.5);
INSERT INTO telemetry (id, temp) VALUES (27, 4.2);
INSERT INTO telemetry (id, temp) VALUES (28, 3.9);
INSERT INTO telemetry (id, temp) VALUES (29, 116.6);
INSERT INTO telemetry (id, temp) VALUES (30, 95.0);
INSERT INTO telemetry (id, temp) VALUES (31, 152.8);
INSERT INTO telemetry (id, temp) VALUES (32, 15.5);
INSERT INTO telemetry (id, temp) VALUES (33, 124.4);
INSERT INTO telemetry (id, temp) VALUES (34, 11.1);
INSERT INTO telemetry (id, temp) VALUES (35, 126.2);
INSERT INTO telemetry (id, temp) VALUES (36, 14.6);
INSERT INTO telemetry (id, temp) VALUES (37, 99.3);
INSERT INTO telemetry (id, temp) VALUES (38, 193.3);
INSERT INTO telemetry (id, temp) VALUES (39, 58.8);
INSERT INTO telemetry (id, temp) VALUES (40, 81.9);
INSERT INTO telemetry (id, temp) VALUES (41, 147.6);
INSERT INTO telemetry (id, temp) VALUES (42, 154.9);
INSERT INTO telemetry (id, temp) VALUES (43, 160.1);
INSERT INTO telemetry (id, temp) VALUES (44, 8.1);
INSERT INTO telemetry (id, temp) VALUES (45, 54.5);
INSERT INTO telemetry (id, temp) VALUES (46, 191.1);
INSERT INTO telemetry (id, temp) VALUES (47, 102.6);
''')
db.commit(); db.close()
PY
