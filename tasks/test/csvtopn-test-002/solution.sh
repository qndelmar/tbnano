cut -d, -f2 items.csv | sort -rn | head -5 | awk '{s+=$1}END{print s}' > answer.txt
