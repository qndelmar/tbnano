awk '!seen[$0]++' dups.txt > dedup.txt
