python3 -c "import sqlite3;print(sqlite3.connect('data.db').execute('select name from sqlite_master').fetchall())"
python3 -c "import sqlite3;print(sqlite3.connect('data.db').execute('SELECT sum(t.v) FROM t JOIN keep ON t.id=keep.id').fetchone()[0])" > answer.txt
cat answer.txt
