cut -d, -f2 items.csv | sort -rn | head -7 | awk '{s+=$1}END{print s}' > answer.txt
