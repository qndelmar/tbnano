cat > filter.sh <<'EOF'
#!/bin/bash
grep ERROR jobs.log > found.txt
EOF
bash filter.sh
