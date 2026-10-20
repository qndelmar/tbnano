sort -t, -k1,1 users.csv > /tmp/u; sort -t, -k1,1 orders.csv > /tmp/o; join -t, /tmp/u /tmp/o > joined.csv
head joined.csv
