sed -i 's/\[main/[main]/' app.ini
python3 -c "import configparser;c=configparser.ConfigParser();c.read('app.ini');print(c['main']['port'])" > out.txt
