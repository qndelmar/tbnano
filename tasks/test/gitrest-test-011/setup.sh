git init -q .
git config user.email t@t && git config user.name t
echo "payload-264" > config.ini
git add -A && git -c user.email=a@b -c user.name=x commit -qm "add config.ini"

git rm -q config.ini && git -c user.email=a@b -c user.name=x commit -qm "remove config.ini"
