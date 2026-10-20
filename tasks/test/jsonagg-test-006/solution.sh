python3 -c "import json;d=json.load(open('records.json'));print(sum(1 for r in d if r['mode']=='queued'))" > answer.txt
