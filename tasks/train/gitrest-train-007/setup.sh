git init -q .
git config user.email t@t && git config user.name t
echo "booster-808" > prefs.ini
git add -A && git -c user.email=a@b -c user.name=x commit -qm "add prefs.ini"

git rm -q prefs.ini && git -c user.email=a@b -c user.name=x commit -qm "remove prefs.ini"
