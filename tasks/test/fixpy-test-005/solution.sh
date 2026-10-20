cat > avg.py <<'EOF'
xs = open('nums.txt').read().split()
s = 0.0
for x in xs:
    s += float(x)
print(s / len(xs))
EOF
python3 avg.py > out.txt
cat out.txt
