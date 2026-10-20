cat > ops.py <<'EOF'
def km_to_miles(km):
    return km * 0.621371
EOF
python3 check.py
