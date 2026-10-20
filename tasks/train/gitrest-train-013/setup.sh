git init -q .
git config user.email t@t && git config user.name t
echo "telemetry-316" > diary.txt
git add -A && git -c user.email=a@b -c user.name=x commit -qm "add diary.txt"

git rm -q diary.txt && git -c user.email=a@b -c user.name=x commit -qm "remove diary.txt"
