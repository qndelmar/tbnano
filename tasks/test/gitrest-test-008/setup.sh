git init -q .
git config user.email t@t && git config user.name t
echo "payload-817" > notes.txt
git add -A && git -c user.email=a@b -c user.name=x commit -qm "add notes.txt"

git rm -q notes.txt && git -c user.email=a@b -c user.name=x commit -qm "remove notes.txt"
