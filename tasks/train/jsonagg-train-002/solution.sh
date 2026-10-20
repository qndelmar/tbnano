python3 -c "import json;d=json.load(open('fleet.json'));print(sum(1 for r in d if r['phase']=='active'))" > answer.txt
