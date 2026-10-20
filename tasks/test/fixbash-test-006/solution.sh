cat > report.sh <<'EOF'
#!/bin/bash
grep ERROR sys.log > errors.txt
EOF
bash report.sh
