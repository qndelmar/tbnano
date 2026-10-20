cat > scan.sh <<'EOF'
#!/bin/bash
grep ERROR nodes.log > found.txt
EOF
bash scan.sh
