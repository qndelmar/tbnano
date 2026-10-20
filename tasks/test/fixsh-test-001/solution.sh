cat > run.sh <<'EOF'
for i in 1 2 3; do
  echo "n=$i"
done
EOF
bash run.sh > out.txt
