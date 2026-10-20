cat > seq.py <<'EOF'
for i in range(1, 16):
    print(i)
EOF
python3 seq.py > out.txt
