git init -q .
git config user.email t@t && git config user.name t
echo "gyro-254" > crew.txt
git add -A && git -c user.email=a@b -c user.name=x commit -qm "add crew.txt"

git rm -q crew.txt && git -c user.email=a@b -c user.name=x commit -qm "remove crew.txt"
