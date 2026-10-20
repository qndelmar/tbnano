cat > report.sh <<'EOF'
#!/bin/bash
grep ERROR sys.log > errs.txt
EOF
bash report.sh
