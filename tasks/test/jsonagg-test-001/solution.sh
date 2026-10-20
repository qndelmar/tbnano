python3 -c "import json;d=json.load(open('inventory.json'));print(sum(1 for r in d if r['mode']=='failed'))" > answer.txt
