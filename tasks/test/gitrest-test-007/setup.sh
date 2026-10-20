git init -q .
git config user.email t@t && git config user.name t
echo "booster-505" > manifest.txt
git add -A && git -c user.email=a@b -c user.name=x commit -qm "add manifest.txt"
echo noise0 > other0.txt && git add -A && git -c user.email=a@b -c user.name=x commit -qm noise0
git rm -q manifest.txt && git -c user.email=a@b -c user.name=x commit -qm "remove manifest.txt"
