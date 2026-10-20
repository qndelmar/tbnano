python3 -c "import csv;v=[float(r['vspeed_fpm']) for r in csv.DictReader(open('log.csv'))];print(max(v)*0.00508)" > answer.txt
