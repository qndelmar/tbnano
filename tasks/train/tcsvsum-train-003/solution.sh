tail -n +2 data.csv | awk '{s+=$1}END{print s}' > answer.txt
