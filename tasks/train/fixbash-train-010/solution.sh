cat > scan.sh <<'EOF'
#!/bin/bash
grep ERROR nodes.log > hits.txt
EOF
bash scan.sh
