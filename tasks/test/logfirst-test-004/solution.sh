grep -n '\[ERROR\]' server.log | head -1 | cut -d: -f1 > answer.txt
