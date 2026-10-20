git init -q .
git config user.email t@t && git config user.name t
echo "payload-618" > prefs.ini
git add -A && git -c user.email=a@b -c user.name=x commit -qm "add prefs.ini"
echo noise0 > other0.txt && git add -A && git -c user.email=a@b -c user.name=x commit -qm noise0
git rm -q prefs.ini && git -c user.email=a@b -c user.name=x commit -qm "remove prefs.ini"
