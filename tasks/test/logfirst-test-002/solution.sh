grep -n '\[ERROR\]' daemon.log | head -1 | cut -d: -f1 > answer.txt
