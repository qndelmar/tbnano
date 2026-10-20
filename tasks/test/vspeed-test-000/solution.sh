tail -n +2 telem.csv | cut -d, -f2 | sort -rn | head -1 > answer.txt
