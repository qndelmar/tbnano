grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' frontend.log | sort -u > sources.txt
