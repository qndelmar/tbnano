cat > run.sh <<'EOF'
echo $((1 + 2))
EOF
bash run.sh > out.txt
