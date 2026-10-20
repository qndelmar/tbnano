git init -q .
git config user.email t@t && git config user.name t
echo "telemetry-951" > manifest.txt
git add -A && git -c user.email=a@b -c user.name=x commit -qm "add manifest.txt"

git rm -q manifest.txt && git -c user.email=a@b -c user.name=x commit -qm "remove manifest.txt"
