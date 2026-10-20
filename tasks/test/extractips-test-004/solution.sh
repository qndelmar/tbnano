grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' edge.log | sort -u > ips.txt
