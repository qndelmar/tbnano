grep '\[ERROR\]' app.log | awk -F'T' '{print $2}' | cut -d: -f1 | awk '$1>=12 && $1<=21' | wc -l > answer.txt
