grep -n '\[ERROR\]' svc.log | head -1 | cut -d: -f1 > answer.txt
