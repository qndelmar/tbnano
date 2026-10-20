python3 -c "import json;d=json.load(open('items.json'));print(sum(1 for r in d if r['kind']=='failed'))" > answer.txt
