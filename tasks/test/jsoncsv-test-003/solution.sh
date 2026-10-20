python3 -c "import json;d=json.load(open('records.json'));print('id,v');[print(f\"{x['id']},{x['v']}\") for x in d]" > out.csv
head out.csv
