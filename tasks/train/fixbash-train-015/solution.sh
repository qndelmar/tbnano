cat > filter.sh <<'EOF'
#!/bin/bash
grep ERROR nodes.log > found.txt
EOF
bash filter.sh
