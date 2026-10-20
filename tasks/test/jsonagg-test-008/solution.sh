python3 -c "import json;d=json.load(open('events.json'));print(sum(r['value'] for r in d if r['state']=='active'))" > answer.txt
