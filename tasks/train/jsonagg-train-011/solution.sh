python3 -c "import json;d=json.load(open('items.json'));print(sum(r['value'] for r in d if r['phase']=='failed'))" > answer.txt
