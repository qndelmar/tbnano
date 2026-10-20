python3 -c "import csv;v=[float(r['speed_kt']) for r in csv.DictReader(open('flight.csv'))];print(max(v)*1.852)" > answer.txt
