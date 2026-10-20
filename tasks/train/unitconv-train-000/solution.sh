python3 -c "import csv;v=[float(r['alt_ft']) for r in csv.DictReader(open('series.csv'))];print(sum(v)/len(v)*0.3048)" > answer.txt
