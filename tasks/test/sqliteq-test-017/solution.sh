python3 -c "import sqlite3;print(sqlite3.connect('db.sqlite').execute('select count(*) from events where pressure>150').fetchone()[0])" > answer.txt
