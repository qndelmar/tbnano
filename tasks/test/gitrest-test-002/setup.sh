git init -q . && git config user.email t@t && git config user.name t
printf 'x=81\n' > cfg.txt && git add cfg.txt && git commit -qm init
printf 'x=BROKEN\n' > cfg.txt
