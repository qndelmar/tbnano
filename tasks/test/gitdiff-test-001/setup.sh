git init -q . && git config user.email t@t && git config user.name t
seq 1 20 > f.txt && git add f.txt && git commit -qm init
sed -i '1,8d' f.txt
seq 21 23 >> f.txt
