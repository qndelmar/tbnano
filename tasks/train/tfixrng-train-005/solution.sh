cat > sq.py <<'EOF'
for i in range(8):
    print(i * i)
EOF
python3 sq.py > out.txt
