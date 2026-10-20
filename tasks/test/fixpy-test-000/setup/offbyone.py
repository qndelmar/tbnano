xs = [int(x) for x in open('nums.txt')]
print(sum(xs[:len(xs)-1]))
