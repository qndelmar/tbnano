python3 -c "import json;d=json.load(open('metrics.json'));print(sum(x['watt'] for x in d if x['on']))" > answer.txt
