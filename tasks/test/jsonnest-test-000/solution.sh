python3 -c 'import json;print(json.load(open("nest.json"))[0])'
python3 -c "import json;d=json.load(open('nest.json'));print(sum(x['meta']['score'] for x in d if x['id']%2==0))" > answer.txt
cat answer.txt
