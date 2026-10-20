python3 -c "import json;d=json.load(open('records.json'));print(sum(r['value'] for r in d if r['mode']=='retired'))" > answer.txt
