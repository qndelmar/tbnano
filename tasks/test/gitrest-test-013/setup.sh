git init -q .
git config user.email t@t && git config user.name t
echo "hyperdrive-530" > config.ini
git add -A && git -c user.email=a@b -c user.name=x commit -qm "add config.ini"
echo noise0 > other0.txt && git add -A && git -c user.email=a@b -c user.name=x commit -qm noise0
git rm -q config.ini && git -c user.email=a@b -c user.name=x commit -qm "remove config.ini"
