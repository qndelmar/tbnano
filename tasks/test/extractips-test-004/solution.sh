grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' access.log | sort -u > clients.txt
