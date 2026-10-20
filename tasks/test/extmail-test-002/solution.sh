grep -oE 'from=<[^>]+>' maillog.txt | sed 's/from=<//;s/>//' | sort -u > senders.txt
