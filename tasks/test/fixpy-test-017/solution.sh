cat > utils.py <<'EOF'
def area_circle(r):
    return 3.14159 * r ** 2
EOF
python3 check.py
