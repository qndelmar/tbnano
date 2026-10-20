python3 -c "import csv;v=[float(r['pressure_psi']) for r in csv.DictReader(open('log.csv'))];print(max(v)*6.894757)" > answer.txt
