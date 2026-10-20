python3 -c "import json;d=json.load(open('events.json'));print(sum(r['value'] for r in d if r['status']=='failed'))" > answer.txt
