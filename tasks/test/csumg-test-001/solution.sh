awk -F, 'NR>1{s+=$2}END{print s}' vals.csv > answer.txt
