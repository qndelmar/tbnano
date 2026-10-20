cat > offbyone.py <<'EOF'
xs = [int(x) for x in open('nums.txt')]
print(sum(xs))
EOF
python3 offbyone.py > out.txt
cat out.txt
