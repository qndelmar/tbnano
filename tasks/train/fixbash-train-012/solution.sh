cat > filter.sh <<'EOF'
#!/bin/bash
grep ERROR jobs.log > hits.txt
EOF
bash filter.sh
