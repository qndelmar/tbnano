xs = open('nums.txt').read().split()
s = 0
for x in xs:
    s += x
print(s / len(xs))
