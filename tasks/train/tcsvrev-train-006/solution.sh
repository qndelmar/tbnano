awk -F, '{print $2","$1}' pairs.csv > rev.csv
