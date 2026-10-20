python3 -c "import json;d=json.load(open('inventory.json'));print(sum(r['value'] for r in d if r['mode']=='active'))" > answer.txt
