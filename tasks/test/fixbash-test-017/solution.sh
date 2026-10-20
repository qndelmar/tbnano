cat > extract.sh <<'EOF'
#!/bin/bash
grep ERROR sys.log > errors.txt
EOF
bash extract.sh
