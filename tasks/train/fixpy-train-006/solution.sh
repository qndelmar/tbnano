cat > helpers.py <<'EOF'
def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x
EOF
python3 check.py
