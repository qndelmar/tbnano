cat > compute.py <<'EOF'
def sum_evens(xs):
    return sum(x for x in xs if x % 2 == 0)
EOF
python3 check.py
