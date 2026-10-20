python3 -c "import json;d=json.load(open('events.json'));print(sum(1 for r in d if r['status']=='active'))" > answer.txt
