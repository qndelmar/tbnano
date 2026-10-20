python3 -c "import csv;v=[float(r['mass_lbs']) for r in csv.DictReader(open('series.csv'))];print(max(v)*0.45359237)" > answer.txt
