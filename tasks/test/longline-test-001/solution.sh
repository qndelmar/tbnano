awk '{if(length($0)>m)m=length($0)}END{print m}' notes.txt > answer.txt
