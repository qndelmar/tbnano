cat > scan.sh <<'EOF'
#!/bin/bash
grep ERROR jobs.log > found.txt
EOF
bash scan.sh
