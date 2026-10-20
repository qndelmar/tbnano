sed -i 's/,}/}/' conf.json
python3 -c "import json;print(json.load(open('conf.json'))['port'])" > out.txt
