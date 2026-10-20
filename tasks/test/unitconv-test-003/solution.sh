python3 -c "import csv;v=[float(r['alt_ft']) for r in csv.DictReader(open('log.csv'))];print(sum(v)/len(v)*0.3048)" > answer.txt
