cat > f.py <<'EOF'
x = 4
if x > 0:
    print(x)
else:
    print(0)
EOF
python3 f.py > out.txt
