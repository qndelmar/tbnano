cat > seq.py <<'EOF'
for i in range(1, 6):
    print(i)
EOF
python3 seq.py > out.txt
