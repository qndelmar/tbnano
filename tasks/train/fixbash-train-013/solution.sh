cat > filter.sh <<'EOF'
#!/bin/bash
grep ERROR nodes.log > hits.txt
EOF
bash filter.sh
