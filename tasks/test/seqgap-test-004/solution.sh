python3 -c "v=[int(l) for l in open('ids.txt')];print(set(range(v[0],v[-1]+1))-set(v))" | tr -d '{} ' > answer.txt
