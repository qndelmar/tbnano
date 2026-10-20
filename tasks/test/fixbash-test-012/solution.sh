cat > extract.sh <<'EOF'
#!/bin/bash
grep ERROR app.log > errs.txt
EOF
bash extract.sh
