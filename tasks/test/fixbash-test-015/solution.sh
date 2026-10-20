cat > extract.sh <<'EOF'
#!/bin/bash
grep ERROR sys.log > errs.txt
EOF
bash extract.sh
