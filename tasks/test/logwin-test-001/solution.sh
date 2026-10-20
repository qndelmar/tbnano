grep '\[ERROR\]' daemon.log | awk -F'T' '{print $2}' | cut -d: -f1 | awk '$1>=0 && $1<=5' | wc -l > answer.txt
