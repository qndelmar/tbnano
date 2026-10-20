python3 - <<'PY'
import sqlite3
db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE channels (id INTEGER PRIMARY KEY, current REAL)')
db.executescript('''
INSERT INTO channels (id, current) VALUES (1, 47.9);
INSERT INTO channels (id, current) VALUES (2, 95.1);
INSERT INTO channels (id, current) VALUES (3, 135.1);
INSERT INTO channels (id, current) VALUES (4, 141.5);
INSERT INTO channels (id, current) VALUES (5, 65.3);
INSERT INTO channels (id, current) VALUES (6, 172.1);
INSERT INTO channels (id, current) VALUES (7, 58.0);
INSERT INTO channels (id, current) VALUES (8, 146.0);
INSERT INTO channels (id, current) VALUES (9, 71.3);
INSERT INTO channels (id, current) VALUES (10, 126.4);
INSERT INTO channels (id, current) VALUES (11, 47.7);
INSERT INTO channels (id, current) VALUES (12, 78.6);
INSERT INTO channels (id, current) VALUES (13, 184.1);
INSERT INTO channels (id, current) VALUES (14, 76.5);
INSERT INTO channels (id, current) VALUES (15, 23.3);
INSERT INTO channels (id, current) VALUES (16, 198.3);
INSERT INTO channels (id, current) VALUES (17, 193.3);
INSERT INTO channels (id, current) VALUES (18, 174.3);
INSERT INTO channels (id, current) VALUES (19, 18.4);
INSERT INTO channels (id, current) VALUES (20, 183.8);
INSERT INTO channels (id, current) VALUES (21, 195.6);
INSERT INTO channels (id, current) VALUES (22, 150.7);
INSERT INTO channels (id, current) VALUES (23, 118.1);
INSERT INTO channels (id, current) VALUES (24, 63.8);
INSERT INTO channels (id, current) VALUES (25, 134.2);
INSERT INTO channels (id, current) VALUES (26, 52.9);
INSERT INTO channels (id, current) VALUES (27, 162.7);
INSERT INTO channels (id, current) VALUES (28, 108.9);
INSERT INTO channels (id, current) VALUES (29, 144.7);
INSERT INTO channels (id, current) VALUES (30, 163.0);
INSERT INTO channels (id, current) VALUES (31, 91.5);
INSERT INTO channels (id, current) VALUES (32, 95.3);
INSERT INTO channels (id, current) VALUES (33, 51.1);
INSERT INTO channels (id, current) VALUES (34, 128.6);
INSERT INTO channels (id, current) VALUES (35, 30.6);
INSERT INTO channels (id, current) VALUES (36, 67.9);
INSERT INTO channels (id, current) VALUES (37, 144.9);
INSERT INTO channels (id, current) VALUES (38, 157.7);
INSERT INTO channels (id, current) VALUES (39, 175.1);
INSERT INTO channels (id, current) VALUES (40, 60.2);
INSERT INTO channels (id, current) VALUES (41, 52.4);
INSERT INTO channels (id, current) VALUES (42, 90.3);
INSERT INTO channels (id, current) VALUES (43, 165.3);
INSERT INTO channels (id, current) VALUES (44, 31.8);
INSERT INTO channels (id, current) VALUES (45, 56.7);
INSERT INTO channels (id, current) VALUES (46, 61.0);
INSERT INTO channels (id, current) VALUES (47, 106.3);
INSERT INTO channels (id, current) VALUES (48, 101.1);
INSERT INTO channels (id, current) VALUES (49, 150.7);
INSERT INTO channels (id, current) VALUES (50, 52.8);
INSERT INTO channels (id, current) VALUES (51, 51.1);
INSERT INTO channels (id, current) VALUES (52, 152.1);
INSERT INTO channels (id, current) VALUES (53, 119.7);
INSERT INTO channels (id, current) VALUES (54, 85.7);
INSERT INTO channels (id, current) VALUES (55, 98.7);
INSERT INTO channels (id, current) VALUES (56, 139.7);
INSERT INTO channels (id, current) VALUES (57, 99.7);
INSERT INTO channels (id, current) VALUES (58, 65.0);
INSERT INTO channels (id, current) VALUES (59, 42.4);
INSERT INTO channels (id, current) VALUES (60, 103.3);
INSERT INTO channels (id, current) VALUES (61, 86.0);
INSERT INTO channels (id, current) VALUES (62, 136.3);
INSERT INTO channels (id, current) VALUES (63, 143.9);
INSERT INTO channels (id, current) VALUES (64, 134.0);
INSERT INTO channels (id, current) VALUES (65, 128.6);
INSERT INTO channels (id, current) VALUES (66, 83.3);
INSERT INTO channels (id, current) VALUES (67, 128.4);
INSERT INTO channels (id, current) VALUES (68, 75.9);
INSERT INTO channels (id, current) VALUES (69, 109.1);
INSERT INTO channels (id, current) VALUES (70, 166.2);
INSERT INTO channels (id, current) VALUES (71, 22.1);
INSERT INTO channels (id, current) VALUES (72, 114.0);
INSERT INTO channels (id, current) VALUES (73, 122.5);
INSERT INTO channels (id, current) VALUES (74, 47.4);
INSERT INTO channels (id, current) VALUES (75, 26.6);
INSERT INTO channels (id, current) VALUES (76, 46.2);
INSERT INTO channels (id, current) VALUES (77, 7.5);
INSERT INTO channels (id, current) VALUES (78, 57.6);
INSERT INTO channels (id, current) VALUES (79, 74.7);
INSERT INTO channels (id, current) VALUES (80, 181.3);
''')
db.commit(); db.close()
PY
