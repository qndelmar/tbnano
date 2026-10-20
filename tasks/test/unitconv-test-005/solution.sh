python3 -c "import csv;v=[float(r['vspeed_fpm']) for r in csv.DictReader(open('telemetry.csv'))];print(sum(v)/len(v)*0.00508)" > answer.txt
