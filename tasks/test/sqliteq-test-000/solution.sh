python3 -c "import sqlite3;print(sqlite3.connect('db.sqlite').execute('select count(*) from telemetry where temp>20').fetchone()[0])" > answer.txt
