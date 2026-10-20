grep -oE 'GET [^ ]+' crawl.log | sed 's/^GET //' | sort -u > urls.txt
