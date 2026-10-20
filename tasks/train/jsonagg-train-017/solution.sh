python3 -c "import json;d=json.load(open('jobs.json'));print(sum(1 for r in d if r['flag']=='failed'))" > answer.txt
