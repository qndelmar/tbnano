awk -F, '{print $2","$1}' m.csv > swapped.csv
