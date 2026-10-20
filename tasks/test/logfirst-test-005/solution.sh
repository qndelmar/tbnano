grep -n '\[ERROR\]' app.log | head -1 | cut -d: -f1 > answer.txt
