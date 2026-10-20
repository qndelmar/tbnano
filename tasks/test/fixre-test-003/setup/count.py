import re, sys
lines = [l for l in open('in.txt') if re.search(r'[0-9+', l)]
print(len(lines))
