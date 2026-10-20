cat > report.sh <<'EOF'
#!/bin/bash
grep ERROR app.log > errs.txt
EOF
bash report.sh
