grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' hits.log | sort -u > addrs.txt
