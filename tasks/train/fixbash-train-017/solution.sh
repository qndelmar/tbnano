cat > scan.sh <<'EOF'
#!/bin/bash
grep ERROR jobs.log > hits.txt
EOF
bash scan.sh
