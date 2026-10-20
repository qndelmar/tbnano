cat > extract.sh <<'EOF'
#!/bin/bash
grep ERROR app.log > errors.txt
EOF
bash extract.sh
