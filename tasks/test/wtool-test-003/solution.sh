cat > count.sh <<'EOF'
grep -c '^fail$' results.txt
EOF
bash count.sh > out.txt
cat out.txt
