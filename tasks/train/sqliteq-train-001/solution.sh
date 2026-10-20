python3 -c "import sqlite3;print(sqlite3.connect('db.sqlite').execute('select count(*) from samples where torque>20').fetchone()[0])" > answer.txt
