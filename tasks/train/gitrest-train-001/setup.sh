git init -q .
git config user.email t@t && git config user.name t
echo "gyro-515" > team.txt
git add -A && git -c user.email=a@b -c user.name=x commit -qm "add team.txt"

git rm -q team.txt && git -c user.email=a@b -c user.name=x commit -qm "remove team.txt"
