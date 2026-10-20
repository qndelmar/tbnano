grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' requests.log | sort -u > ips.txt
