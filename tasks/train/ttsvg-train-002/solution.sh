awk -F'\t' 'NR>1{s+=$2}END{print s}' vals.tsv > answer.txt
