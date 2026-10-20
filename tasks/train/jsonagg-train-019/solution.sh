python3 -c "import json;d=json.load(open('fleet.json'));print(sum(r['value'] for r in d if r['phase']=='idle'))" > answer.txt
