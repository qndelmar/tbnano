python3 -c "v=[float(l) for l in open('data.csv')];open('stats.txt','w').write(f'min={min(v)}\nmax={max(v)}\nsum={sum(v)}\n')"
cat stats.txt
