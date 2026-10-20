python3 -c "import csv;v=[float(r['pressure_psi']) for r in csv.DictReader(open('series.csv'))];print(sum(v)/len(v)*6.894757)" > answer.txt
