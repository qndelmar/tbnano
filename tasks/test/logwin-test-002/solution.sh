grep '\[WARN\]' daemon.log | awk -F'T' '{print $2}' | cut -d: -f1 | awk '$1>=2 && $1<=16' | wc -l > answer.txt
