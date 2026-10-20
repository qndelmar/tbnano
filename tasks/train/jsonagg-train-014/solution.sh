python3 -c "import json;d=json.load(open('jobs.json'));print(sum(r['value'] for r in d if r['flag']=='idle'))" > answer.txt
