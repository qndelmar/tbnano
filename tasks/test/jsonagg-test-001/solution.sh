python3 -c "import json;d=json.load(open('metrics.json'));print(sum(x['temp'] for x in d if x['on']))" > answer.txt
