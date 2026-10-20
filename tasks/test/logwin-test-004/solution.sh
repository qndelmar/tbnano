grep '\[ERROR\]' server.log | awk -F'T' '{print $2}' | cut -d: -f1 | awk '$1>=4 && $1<=19' | wc -l > answer.txt
