cat > report.sh <<'EOF'
#!/bin/bash
grep ERROR app.log > errors.txt
EOF
bash report.sh
