awk '{if(length($0)>m)m=length($0)}END{print m}' blob.txt > answer.txt
