python3 -c "import sqlite3;print(sqlite3.connect('m.db').execute('SELECT max(v) FROM t').fetchone()[0])" > answer.txt
