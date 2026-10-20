cat > sq.py <<'EOF'
for i in range(3):
    print(i * i)
EOF
python3 sq.py > out.txt
