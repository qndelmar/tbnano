git init -q .
git config user.email t@t && git config user.name t
echo "telemetry-608" > diary.txt
git add -A && git -c user.email=a@b -c user.name=x commit -qm "add diary.txt"
echo noise0 > other0.txt && git add -A && git -c user.email=a@b -c user.name=x commit -qm noise0
git rm -q diary.txt && git -c user.email=a@b -c user.name=x commit -qm "remove diary.txt"
