grep -n '\[ERROR\]' system.log | head -1 | cut -d: -f1 > answer.txt
