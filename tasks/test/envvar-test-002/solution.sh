cat .key
RUN_KEY=$(cat .key) python3 app.py > out.txt
