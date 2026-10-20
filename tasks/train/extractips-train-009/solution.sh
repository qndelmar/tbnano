grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' traffic.log | sort -u > addrs.txt
