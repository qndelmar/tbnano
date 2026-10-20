cat > utils.py <<'EOF'
def moving_average(xs, k):
    return [sum(xs[i:i+k]) / k for i in range(len(xs) - k + 1)]
EOF
python3 check.py
