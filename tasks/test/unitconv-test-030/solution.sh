python3 -c "import csv;v=[float(r['speed_kt']) for r in csv.DictReader(open('log.csv'))];print(sum(v)/len(v)*1.852)" > answer.txt
