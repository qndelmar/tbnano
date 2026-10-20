git init -q .
git config user.email t@t && git config user.name t
echo "hyperdrive-558" > index.txt
git add -A && git -c user.email=a@b -c user.name=x commit -qm "add index.txt"
echo noise0 > other0.txt && git add -A && git -c user.email=a@b -c user.name=x commit -qm noise0
git rm -q index.txt && git -c user.email=a@b -c user.name=x commit -qm "remove index.txt"
