grep '\[ERROR\]' app.log | awk -F'T' '{print $2}' | cut -d: -f1 | awk '$1>=6 && $1<=14' | wc -l > answer.txt
